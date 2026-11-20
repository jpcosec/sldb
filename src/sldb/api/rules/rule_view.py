"""The graph view a `RuleGraph` evaluates over, adjusted for a write: declared edges swapped in,
and the document the index does not hold yet."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.store.edge_index.node_ids import bare
from sldb.store.graph.language.predicate_view import edge, node as view_node

_DECLARED = ("references", "contains")


def declared_view(view: dict[str, Any], declared: tuple[str, tuple[Any, ...]] | None) -> dict[str, Any]:
    """`view`, where the declared edges of the `declared` node are the new ones."""
    if declared is None:
        return view
    node, new = declared
    added = [edge(bare(e.source), e.relation, bare(e.target), e.metadata.get("field"), e.metadata.get("declared")) for e in new]
    replaced = lambda e: e["source"] == node and e["type"] in _DECLARED  # noqa: E731
    out = lambda i: [e for e in view["out"](i) if not replaced(e)] + [e for e in added if e["source"] == i]  # noqa: E731
    into = lambda i: [e for e in view["in"](i) if not replaced(e)] + [e for e in added if e["target"] == i]  # noqa: E731
    return {**view, "out": out, "in": into}


def unindexed(store_path: Path, node: str) -> dict[str, Any]:
    """A document the index does not hold yet: its family from the store's model registry
    (`indexed_model_bases`, no class imported), so `model <= Base` reads as for an indexed one."""
    from sldb.api.stores.resolve_indexed_document import indexed_model_bases

    model = node.rsplit(":", 1)[0].rsplit(":", 1)[-1]
    return view_node(node, model, {}, indexed_model_bases(store_path).get(model, []))
