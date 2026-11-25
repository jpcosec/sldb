"""`model_tag` over a composed edge index: the model nodes' tags and the `semantic_parent` and
`semantic_equivalent` edges between tag nodes (the DAG `sldb semantic show` reads)."""

from __future__ import annotations

from typing import Any

from sldb.store.edge_index.node_ids import bare, model_node_id, tag_node_id
from sldb.store.graph.language.semantic_scope import scope


def index_semantics(index: Any) -> dict[str, Any]:
    """The view entries `model_tags`, `tag_known` and `tag_scope` of `index` (None: empty)."""
    return {
        "model_tags": lambda model: _model_tags(index, model),
        "tag_known": lambda tag: index is not None and index.node(tag_node_id(tag)) is not None,
        "tag_scope": lambda tag: scope(tag, lambda t: _below(index, t), lambda t: _equal(index, t)),
    }


def _model_tags(index: Any, model: str) -> set[str]:
    record = index.node(model_node_id(model)) if index is not None else None
    return set(record.semantics.get("semantic_tags") or []) if record is not None else set()


def _below(index: Any, tag: str) -> list[str]:
    return [bare(e.source) for e in index.edges_to(tag_node_id(tag), "semantic_parent")] if index is not None else []


def _equal(index: Any, tag: str) -> list[str]:
    if index is None:
        return []
    node = tag_node_id(tag)
    return [bare(e.target) for e in index.edges_from(node, "semantic_equivalent")] + [bare(e.source) for e in index.edges_to(node, "semantic_equivalent")]
