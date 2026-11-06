"""The minimal graph view the evaluator reads (p8): nodes, and edges out of and into a node.

A view is a dict of four callables: `node(id)` (a node dict or None), `out(id)` and `in(id)`
(edge dicts: `source`, `type`, `target`, `field`, `declared`, `unavailable`) and `ids()` (the
documents of the domain). `graph_view` builds it from the test graph of rules-language.md §8
(H2); `NetworkXBackend` builds one over the composed index (`backend/index_view.py`).
"""

from __future__ import annotations

from typing import Any


def make_view(nodes: dict[str, dict], edges: list[dict]) -> dict[str, Any]:
    """A view over node dicts by id and edge dicts."""
    out, into = _by(edges, "source"), _by(edges, "target")
    return {"node": nodes.get, "out": lambda i: out.get(i, []), "in": lambda i: into.get(i, []), "ids": lambda: sorted(nodes)}


def node(node_id: str, model: str | None, payload: dict, base_models=(), name: str | None = None) -> dict[str, Any]:
    """A node of a view."""
    return {"id": node_id, "model": model, "base_models": list(base_models), "payload": payload, "name": node_id.rsplit(":", 1)[-1] if name is None else name}


def edge(source: str, type_: str, target: str, field: str | None = None, declared: Any = None, unavailable: bool = False) -> dict[str, Any]:
    """An edge of a view; `declared` is the value the origin's field wrote (default: target)."""
    return {"source": source, "type": type_, "target": target, "field": field, "declared": target if declared is None else declared, "unavailable": unavailable}


def graph_view(graph: dict) -> dict[str, Any]:
    """The view of `{nodes: {id: {model, payload, base_models?}}, edges: [{source, type, target, field?, unavailable?}]}`."""
    nodes = {i: node(i, n.get("model"), dict(n.get("payload") or {}), n.get("base_models") or ()) for i, n in graph.get("nodes", {}).items()}
    edges = [edge(e["source"], e["type"], e["target"], e.get("field"), e.get("declared"), bool(e.get("unavailable"))) for e in graph.get("edges", [])]
    return make_view(nodes, edges)


def with_node(view: dict[str, Any], replacement: dict) -> dict[str, Any]:
    """`view` where the node of `replacement["id"]` reads as `replacement`."""
    read = view["node"]
    return {**view, "node": lambda i: replacement if i == replacement["id"] else read(i)}


def _by(edges: list[dict], key: str) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for item in edges:
        grouped.setdefault(item[key], []).append(item)
    return grouped
