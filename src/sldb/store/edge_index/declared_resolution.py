"""Point each declared reference at the document it names, or report it.

A shard records a declared value as written (`declared_references`). Which document a bare id
or a path names depends on what else is tracked, so it is decided here, when the index is
composed, like the other rules that span documents:

1. an export id (`Model:name`) is used as written;
2. a path a tracked document lives at names that document;
3. a bare id is tried as `Model:id` for each model the field allows: one match resolves it,
   several are `ambiguous`, none is `missing_document`.

A value that names nothing becomes an `UnresolvedReference`, never an edge. A free reference
field (no allowed models) only reports what is clearly meant as a document: an export id, or
a path in a field that declares models.
"""

from __future__ import annotations

from sldb.store.edge_index.composition_targets import _normalized, _owners_by_path
from sldb.store.edge_index.declared_references import CONTAINS, PENDING_TARGET, is_export_id, looks_like_path
from sldb.store.edge_index.node_ids import doc_node_id
from sldb.store.edge_index.unresolved_reference import UnresolvedReference
from sldb.store.models import EdgeNodeRecord, EdgeRecord

_DOC = "sldb://document/"


def resolve_declared_edges(nodes: dict[str, EdgeNodeRecord], edges: list[EdgeRecord]) -> tuple[list[EdgeRecord], list[UnresolvedReference]]:
    """(every edge, each declared one pointed at its document or left out; what named nothing)."""
    owners = _owners_by_path(nodes)
    kept: list[EdgeRecord] = []
    unresolved: list[UnresolvedReference] = []
    for e in edges:
        if "declared" not in e.metadata or e.metadata.get("origin") != "schema":
            kept.append(e)
        else:
            _place(e, nodes, owners, kept, unresolved)
    return kept, unresolved


def _place(e: EdgeRecord, nodes: dict, owners: dict[str, str], kept: list[EdgeRecord], unresolved: list[UnresolvedReference]) -> None:
    """The declared edge, pointed at its document; or its report; or nothing (a free field's value)."""
    target, reason, export_id = _resolve(e, nodes, owners)
    if target is not None:
        kept.append(EdgeRecord(source=e.source, target=target, relation=e.relation, metadata=e.metadata))
    elif reason is not None:
        unresolved.append(_report(e, nodes, reason, export_id))


def _resolve(e: EdgeRecord, nodes: dict, owners: dict[str, str]) -> tuple[str | None, str | None, str | None]:
    """(target node id or None, why not, the export id the value names when known)."""
    value, allowed = e.metadata["declared"], list(e.metadata.get("allowed_models") or [])
    if not e.target.startswith(PENDING_TARGET):
        return _by_export_id(e.target, nodes)
    store = _store_of(e.source)
    owner = owners.get(_normalized(value)) if store is None else None
    if owner is not None:
        return owner, None, None
    if looks_like_path(value):
        return None, ("unknown_path" if allowed or e.relation == CONTAINS else None), None
    return _by_allowed_models(value, allowed, store, nodes)


def _by_export_id(target: str, nodes: dict) -> tuple[str | None, str | None, str | None]:
    found = target in nodes
    return (target if found else None), (None if found else "missing_document"), target[len(_DOC):]


def _by_allowed_models(value: str, allowed: list[str], store: str | None, nodes: dict) -> tuple[str | None, str | None, str | None]:
    prefix = f"{store}:" if store else ""
    ids = [f"{prefix}{model}:{value}" for model in allowed]
    hits = [doc_node_id(i) for i in ids if doc_node_id(i) in nodes]
    if len(hits) == 1:
        return hits[0], None, None
    if len(hits) > 1:
        return None, "ambiguous", None
    return None, ("missing_document" if allowed else None), (ids[0] if len(ids) == 1 else None)


def _store_of(source: str) -> str | None:
    """The link name of a linked store's document (`sldb://document/store:Model:name`)."""
    parts = source[len(_DOC):].split("#", 1)[0].split(":")
    return parts[0] if source.startswith(_DOC) and len(parts) == 3 else None


def _report(e: EdgeRecord, nodes: dict, reason: str, export_id: str | None) -> UnresolvedReference:
    source = nodes.get(e.source)
    semantics = source.semantics if source is not None else {}
    export = e.source[len(_DOC):] if e.source.startswith(_DOC) else e.source
    return UnresolvedReference(source=export, model=semantics.get("model") or export.rsplit(":", 2)[-2], field=e.metadata.get("field", ""), target=e.metadata["declared"],
                               target_export_id=export_id, relation="contains" if e.relation == CONTAINS else "references", reason=reason, source_path=semantics.get("path"))


__all__ = ["resolve_declared_edges", "is_export_id"]
