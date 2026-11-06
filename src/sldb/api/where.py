"""The predicate language as a library (GO05): one predicate on a payload, or over a store.

`where_matches` is the language on a plain payload; `where_records` is `sldb find --where`
over search records; `where_findings` evaluates over a store's graph (`GraphBackend.eval`):
paths follow the edge index and payloads come from its projection, nothing is re-extracted.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any

from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.graph.analyze import backend_for
from sldb.api.records.record_filters import RecordFilters
from sldb.api.stores.open_store import open_store
from sldb.store.edge_index.node_ids import bare, kind
from sldb.store.graph.backend.index_view import index_view
from sldb.store.graph.language.predicate_documents import EMPTY_VIEW, document_finding, document_node, has_paths, payload_holds


def where_matches(expression: str, payload: dict[str, Any], subject: dict[str, Any] | None = None) -> bool:
    """Whether a predicate holds on `payload` (the language of `sldb find --where`).

    Args:
        expression: A predicate of `docs/architecture/rules-language.md`: `has(f)`,
            `nonempty(f)`, `"x" in f`, `f ~ "re"`, `f = "s"`, `f >= 3`, `and`/`or`/`not`,
            parentheses...; empty always holds. Paths reach nothing: a payload has no graph.
        payload: The fields the predicate reads; need not belong to a tracked document.
        subject: Fills `{field}` placeholders (default: `payload`). A placeholder the subject
            lacks, or holds as a list or dict, makes the expression not hold.

    Raises:
        WherePredicateError: The expression does not parse.
    """
    return payload_holds(expression, payload, subject)


def where_findings(store: str | Path | None, expression: str, subject: str | None = None, include_linked: bool = False) -> list[dict[str, Any]]:
    """`eval(expression, subject)` over a store: the subject's finding (an export id), or one
    per document of the domain (rules-language.md §6). Each finding has node, holds, clause and
    seen. Reads the edge index and its payload projection; never extracts a document."""
    index = load_edge_index(store, include_linked)
    backend = backend_for(open_store(store, mode="readonly").store_path)
    backend.load(index, {bare(n.id): n.payload for n in index.nodes.values() if kind(n.id) == "document"})
    return backend.eval(expression, subject)


def store_view(store: str | Path | None, include_linked: bool = False) -> dict[str, Any]:
    """The predicate language's graph view of a store's edge index (paths of `--where`)."""
    return index_view(load_edge_index(store, include_linked))


def where_records(records: list, expression: str, store: str | Path | None, pythonpath: str | None = None, include_linked: bool = False) -> tuple[list, list[dict[str, Any]]]:
    """`--where` over `sldb find` records: `(kept, findings)`.

    A document record is evaluated by the language on its payload (plus `sldb`, its
    provenance), with paths over the store's index; it is kept only when `holds` is `true`
    (an `incomplete` does not match). Its finding is in `findings`. Field and section records
    keep their own `--where` reading (`RecordFilters`)."""
    view = store_view(store, include_linked) if has_paths(expression) else EMPTY_VIEW
    found = {id(r): document_finding(expression, _record_node(r), view) for r in records if r.kind == "doc"}
    filters = RecordFilters(pythonpath)
    kept = [r for r in records if (found[id(r)]["holds"] == "true" if r.kind == "doc" else filters.matches(r, expression))]
    return kept, list(found.values())


def _record_node(record: Any) -> dict[str, Any]:
    model_type = record.model_type or type(record.model_name or "Model", (), {})
    doc = SimpleNamespace(payload={**record.payload, "sldb": record.provenance or {}}, name=record.doc_name or record.name, model_type=model_type, model_name=record.model_name)
    prefix = "" if record.store_name in ("local", "", None) else f"{record.store_name}:"
    return document_node(doc, f"{prefix}{record.model_name}:{doc.name}")
