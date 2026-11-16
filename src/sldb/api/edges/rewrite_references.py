"""`sldb.api.rewrite_references(store, target, replacement, *, transaction=None, dry_run=False,
pythonpath=None, graph=None, excluded_sources=())` (GD22): every incoming reference of `target` (what `referrers` finds) rewritten to
name `replacement`, or removed when it is None, inside one `sldb.api.transaction` of GD24 (the one
given or its own): a write that fails puts every document back (docs/architecture/references.md).
A scalar field takes the new value (None removes it: the model decides whether it may be null); a
list field has the element replaced in place, or dropped, never duplicated; a mention has the
captured text replaced on its line (`rewrite_mentions`) through `replace_text`. Every new payload
and text is validated in memory first; with `dry_run` that is all: nothing is opened for writing
and the `on_write` rules do not run. `graph` is a project graph built in process, used instead of
the declared one; the documents named in `excluded_sources` are left untouched, fields and mentions.
"""

from __future__ import annotations

from contextlib import nullcontext
from collections.abc import Iterable
from pathlib import Path

from sldb.api.documents.replace_text import replace_text
from sldb.api.documents.transaction import Transaction, transaction as open_transaction
from sldb.api.edges.project_graph.project_graph import ProjectGraph
from sldb.api.edges.referrers import Hit, Target, document_paths, find_hits, optional_graph, resolve_target
from sldb.api.edges.rewrite_plan import Plan, planned_payload, planned_text
from sldb.api.edges.rewrite_report import RewriteReport
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_location import StoreLocation
from sldb.core.exceptions import SLDBDocumentTargetError


def rewrite_references(store: str | Path | None, target: str, replacement: str | None, *, transaction: Transaction | None = None, dry_run: bool = False, pythonpath: str | None = None, graph: ProjectGraph | None = None, excluded_sources: Iterable[str] = ()) -> RewriteReport:
    """Rewrite (or remove) every reference to `target` (what `referrers` accepts); see the module.

    `replacement` is resolved like `target` (a document keeps each value's form), written as given
    when it names nothing, None to remove. `transaction` is an open one over `store` to join.
    `graph` replaces the declared project graph when given. Each of `excluded_sources` names a
    tracked document like `target` does (`Model:name` and its path exclude the same one); its
    fields and mentions are not rewritten.
    Raises `SLDBDocumentTargetError` (unknown or ambiguous target, ambiguous replacement, an
    excluded source that names no tracked document) and `SLDBValidationError` (a rewritten
    payload or text the model refuses); nothing is written then.
    """
    location = open_store(store, mode="readonly" if dry_run else "default")
    graph = graph if graph is not None else optional_graph(location.store_path)
    found = resolve_target(location, graph, target)
    new = None if replacement is None else replacement_target(location, graph, replacement)
    fields, mentions = _included_hits(location, graph, found, excluded_sources)
    plans = [planned_payload(location, pythonpath, export_id, hits, found, new) for export_id, hits in fields.items()]
    texts = [planned_text(location, graph, pythonpath, path, hits, found, new) for path, hits in mentions.items()]
    if not dry_run:
        _write(location, pythonpath, transaction, plans, [(path, hits) for path, hits in mentions.items() if new is not None], graph, found, new)
    return RewriteReport(changed=[c for plan in plans for c in plan[2]] + [c for text in texts for c in text[3]], skipped=[s for text in texts for s in text[4]])


def replacement_target(location: StoreLocation, graph: ProjectGraph | None, given: str) -> Target:
    """`given` resolved like a target; when it names nothing it is kept literal (an ambiguous one is still an error)."""
    try:
        return resolve_target(location, graph, given)
    except SLDBDocumentTargetError as exc:
        if "Ambiguous" in str(exc):
            raise
        return Target(given, None, None, None, None)


def excluded_paths(location: StoreLocation, graph: ProjectGraph | None, sources: Iterable[str]) -> set[str]:
    """The tracked paths (relative to the project) of the documents `sources` name; one that names no tracked document is `SLDBDocumentTargetError`."""
    paths: set[str] = set()
    for source in sources:
        resolved = resolve_target(location, graph, source)
        if resolved.path is None:
            raise SLDBDocumentTargetError(f"Excluded source is not a tracked document: {source}")
        paths.add(resolved.path)
    return paths


def _included_hits(location: StoreLocation, graph: ProjectGraph | None, target: Target, excluded_sources: Iterable[str]) -> tuple[dict[str, list[Hit]], dict[str, list[Hit]]]:
    """The field hits by source and the mention hits by path, without the documents `excluded_sources` name."""
    excluded = excluded_paths(location, graph, excluded_sources)
    fields, mentions = _grouped(find_hits(location, target, graph))
    if not excluded:
        return fields, mentions
    paths = document_paths(location.store_path)
    return {source: hits for source, hits in fields.items() if paths.get(source) not in excluded}, {path: hits for path, hits in mentions.items() if path not in excluded}


def _grouped(hits: list[Hit]) -> tuple[dict[str, list[Hit]], dict[str, list[Hit]]]:
    fields: dict[str, list[Hit]] = {}
    mentions: dict[str, list[Hit]] = {}
    for hit in hits:
        (fields if hit[0].origin == "schema" else mentions).setdefault(hit[0].source, []).append(hit)
    return fields, mentions


def _write(location: StoreLocation, pythonpath: str | None, transaction: Transaction | None, plans: list[Plan], mentions: list[tuple[str, list[Hit]]], graph: ProjectGraph | None, target: Target, replacement: Target | None) -> None:
    """Payloads first, then each mentioning file re-read (a document may be both) and rewritten through `replace_text`."""
    with nullcontext(transaction) if transaction is not None else open_transaction(location.store_path, pythonpath) as tx:
        for path, payload, _ in plans:
            tx.update(path, payload)
        for path, hits in mentions:
            _, text, new_text, _, _ = planned_text(location, graph, pythonpath, path, hits, target, replacement)
            if new_text != text:
                replace_text(location.store_path, path, text, new_text, count=1, transaction=tx, pythonpath=pythonpath)
