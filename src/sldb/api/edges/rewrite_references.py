"""`sldb.api.rewrite_references(store, target, replacement, *, transaction=None, dry_run=False,
pythonpath=None)` (GD22): every incoming reference of `target` (what `referrers` finds) rewritten to
name `replacement`, or removed when it is None, inside one `sldb.api.transaction` of GD24 (the one
given or its own): a write that fails puts every document back (docs/architecture/references.md).
A scalar field takes the new value (None removes it: the model decides whether it may be null); a
list field has the element replaced in place, or dropped, never duplicated; a mention has the
captured text replaced on its line (`rewrite_mentions`) through `replace_text`. Every new payload
and text is validated in memory first; with `dry_run` that is all: nothing is opened for writing
and the `on_write` rules do not run.
"""

from __future__ import annotations

from contextlib import nullcontext
from pathlib import Path
from typing import Any

from sldb.api.documents.document_payload import runtime_document
from sldb.api.documents.replace_text import replace_text
from sldb.api.documents.transaction import Transaction, transaction as open_transaction
from sldb.api.edges.project_graph.project_graph import ProjectGraph
from sldb.api.edges.referrers import Hit, Target, find_hits, matching_documents, optional_graph, resolve_target
from sldb.api.edges.rewrite_mentions import rewritten_text
from sldb.api.edges.rewrite_report import RewriteReport
from sldb.api.edges.rewrite_values import rewritten_payload
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_location import StoreLocation
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBValidationError
from sldb.runtime.validation import validate_model_data_roundtrip, validate_model_input_roundtrip
from sldb.store.source_guard import aggregate_text

Plan = tuple[str, dict[str, Any], list[dict[str, Any]]]
TextPlan = tuple[str, str, str, list[dict[str, Any]], list[dict[str, Any]]]


def rewrite_references(store: str | Path | None, target: str, replacement: str | None, *, transaction: Transaction | None = None, dry_run: bool = False, pythonpath: str | None = None) -> RewriteReport:
    """Rewrite (or remove) every reference to `target` (what `referrers` accepts); see the module.

    `replacement` is resolved like `target` (a document keeps each value's form), written as given
    when it names nothing, None to remove. `transaction` is an open one over `store` to join.
    Raises `SLDBDocumentTargetError` (unknown or ambiguous target, ambiguous replacement) and
    `SLDBValidationError` (a rewritten payload or text the model refuses); nothing is written then.
    """
    location = open_store(store, mode="readonly" if dry_run else "default")
    graph = optional_graph(location.store_path)
    found = resolve_target(location, graph, target)
    new = None if replacement is None else replacement_target(location, graph, replacement)
    fields, mentions = _grouped(find_hits(location, found, graph))
    plans = [_planned_payload(location, pythonpath, export_id, hits, found, new) for export_id, hits in fields.items()]
    texts = [_planned_text(location, graph, pythonpath, path, hits, found, new) for path, hits in mentions.items()]
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


def _grouped(hits: list[Hit]) -> tuple[dict[str, list[Hit]], dict[str, list[Hit]]]:
    fields: dict[str, list[Hit]] = {}
    mentions: dict[str, list[Hit]] = {}
    for hit in hits:
        (fields if hit[0].origin == "schema" else mentions).setdefault(hit[0].source, []).append(hit)
    return fields, mentions


def _planned_payload(location: StoreLocation, pythonpath: str | None, export_id: str, hits: list[Hit], target: Target, replacement: Target | None) -> Plan:
    """(path, new payload, changes) of one referring document, its payload validated under its model."""
    doc = runtime_document(location.store_path, pythonpath, export_id.replace(":", "/", 1))
    payload, changes = rewritten_payload(dict(doc.payload), [(r, v) for r, v in hits if v is not None], target, replacement)
    _check(export_id, _model_type(location, pythonpath, doc.model_name), payload, None)
    return doc.path, payload, changes


def _planned_text(location: StoreLocation, graph: ProjectGraph | None, pythonpath: str | None, path: str, hits: list[Hit], target: Target, replacement: Target | None) -> TextPlan:
    """(path, text, new text, changes, skips) of one mentioning file, a tracked document's new text validated."""
    if (text := aggregate_text(location.project_root, location.project_root / path, path)) is None:
        return path, "", "", [], [{"source": path, "location": None, "reason": "not read: the path resolves outside the project root or is a symlink"}]
    new_text, changes, skips = rewritten_text(text, graph, path, hits, target, replacement)
    for document in matching_documents(location.store_path, path) if new_text != text else []:
        _check(f"{document['model']}:{document['name']}", _model_type(location, pythonpath, document["model"]), None, new_text)
    return path, text, new_text, changes, skips


def _model_type(location: StoreLocation, pythonpath: str | None, model: str) -> type:
    return load_registered_model(location.store_path, model, pythonpath).model_type


def _check(node: str, model_type: type, payload: dict[str, Any] | None, text: str | None) -> None:
    """The new payload (or text) must validate and round-trip under the model, else `SLDBValidationError` and nothing is written."""
    try:
        valid, details = validate_model_data_roundtrip(model_type, payload) if payload is not None else validate_model_input_roundtrip(model_type, text or "")
    except (ValueError, TypeError) as exc:
        raise SLDBValidationError(f"{node}: the rewritten document does not validate under {model_type.__name__}: {exc}") from exc
    if not valid:
        raise SLDBValidationError(f"{node}: the rewritten document does not round-trip under {model_type.__name__}; nothing written", details)


def _write(location: StoreLocation, pythonpath: str | None, transaction: Transaction | None, plans: list[Plan], mentions: list[tuple[str, list[Hit]]], graph: ProjectGraph | None, target: Target, replacement: Target | None) -> None:
    """Payloads first, then each mentioning file re-read (a document may be both) and rewritten through `replace_text`."""
    with nullcontext(transaction) if transaction is not None else open_transaction(location.store_path, pythonpath) as tx:
        for path, payload, _ in plans:
            tx.update(path, payload)
        for path, hits in mentions:
            _, text, new_text, _, _ = _planned_text(location, graph, pythonpath, path, hits, target, replacement)
            if new_text != text:
                replace_text(location.store_path, path, text, new_text, count=1, transaction=tx, pythonpath=pythonpath)
