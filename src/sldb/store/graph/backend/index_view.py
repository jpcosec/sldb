"""The language's graph view (p8) over a composed edge index and its payload projection.

Document nodes are named by export id (`Model:name`). A node's payload is its projection
entry (`load(index, projection)`), else the projection its shard carries (GO04); its family is
its model and every base the model nodes name (`base_models`, transitively). The domain of a
subject-less `eval` is the projection's documents, or every document node when no projection
was loaded (h1). An edge whose metadata says `unavailable` reaches an incomplete element (H4).
"""

from __future__ import annotations

from typing import Any

from sldb.store.edge_index.node_ids import bare, kind, model_node_id
from sldb.store.graph.language.predicate_view import edge, node


def index_view(index: Any, projection: dict[str, dict[str, Any] | None] | None = None) -> dict[str, Any]:
    """The view of `index` (None reads as an empty index)."""
    docs = {bare(n.id): n for n in (index.nodes.values() if index is not None else ()) if kind(n.id) == "document"}
    payloads = projection if projection is not None else {i: n.payload for i, n in docs.items()}
    read = lambda i: _node(index, docs, payloads, i)  # noqa: E731
    return {"node": read, "out": lambda i: _edges(index, i, "edges_from"), "in": lambda i: _edges(index, i, "edges_to"), "ids": lambda: sorted(payloads)}


def _node(index: Any, docs: dict, payloads: dict, export_id: str) -> dict[str, Any] | None:
    if export_id not in docs and export_id not in payloads:
        return None
    record = docs.get(export_id)
    model = record.node_type if record is not None else export_id.rsplit(":", 1)[0].rsplit(":", 1)[-1]
    payload = payloads.get(export_id) if export_id in payloads else record.payload
    return node(export_id, model, dict(payload or {}), family(index, model))


def family(index: Any, model: str) -> list[str]:
    """Every base model of `model`, transitively, as the index's model nodes declare them."""
    found: list[str] = []
    pending = [model]
    while pending and index is not None:
        record = index.node(model_node_id(pending.pop()))
        bases = (record.semantics.get("base_models") or []) if record is not None else []
        new = [b for b in bases if b not in found and b != model]
        found += new
        pending += new
    return found


def _edges(index: Any, export_id: str, direction: str) -> list[dict[str, Any]]:
    if index is None:
        return []
    return [_edge(e) for e in getattr(index, direction)(export_id)]


def _edge(record: Any) -> dict[str, Any]:
    meta = record.metadata
    return edge(bare(record.source), record.relation, bare(record.target), meta.get("field"), meta.get("declared"), bool(meta.get("unavailable")))
