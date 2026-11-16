"""Explained paths: for each hop of a path, the edges that join it and where each came from.

A hop `(a, b)` lists every edge between the two that the relations walked let through:
`a -> b` with direction `forward`, `b -> a` with direction `backward` (only when the walk is
undirected). The mirror of an undirected relation (`metadata.reverse`) is never listed apart:
it is its authored edge, read `backward`. Edges are ordered by origin, relation_doc first, then
schema, structural and alias, an unknown origin last; ties go by relation and then by
relation_doc or field. `provenance` carries `origin`, `relation_doc` (relation_doc origin
only), `field` (schema origin only) and `from_store` (linked stores only); absent keys are
left out, and the edge's `evidence` never enters it.
"""

from __future__ import annotations

import json
from typing import Any

from sldb.store.graph.analysis.paths import path_between, paths_between
from sldb.store.graph.analysis.relations import resolve

PRECEDENCE = ("relation_doc", "schema", "structural", "alias")
_DETAIL = {"relation_doc": "relation_doc", "schema": "field"}


def explained_path(index, source: str, target: str, relations: object = None, directed: bool = False) -> dict[str, Any] | None:
    """`path_between`, explained: `{"path": [ids], "steps": [...]}`, or None."""
    nodes = path_between(index, source, target, relations, directed)
    return None if nodes is None else explain_path(index, nodes, relations, directed)


def explained_paths(index, source: str, target: str, relations: object = None, cutoff: int | None = None, limit: int = 10) -> list[dict[str, Any]]:
    """`paths_between`, each route explained like `explained_path`."""
    return [explain_path(index, nodes, relations) for nodes in paths_between(index, source, target, relations, cutoff, limit)]


def explain_path(index, nodes: list[str], relations: object = None, directed: bool = False) -> dict[str, Any]:
    """One step per consecutive pair of `nodes`: `{source, target, edges}`."""
    kept = resolve(index, relations)
    steps = [{"source": a, "target": b, "edges": _edges(index, a, b, kept, directed)} for a, b in zip(nodes, nodes[1:])]
    return {"path": list(nodes), "steps": steps}


def _edges(index, a: str, b: str, kept: set[str], directed: bool) -> list[dict[str, Any]]:
    found = [_item(e, not e.metadata.get("reverse")) for e in index.edges_from(a) if e.target == b and e.relation in kept]
    if not directed:
        found += [_item(e, bool(e.metadata.get("reverse"))) for e in index.edges_from(b) if e.target == a and e.relation in kept]
    unique = {json.dumps(item, sort_keys=True, default=str): item for item in found}
    return sorted(unique.values(), key=_rank)


def _item(edge, forward: bool) -> dict[str, Any]:
    return {"relation": edge.relation, "direction": "forward" if forward else "backward", "provenance": _provenance(edge.metadata)}


def _provenance(meta: dict[str, Any]) -> dict[str, Any]:
    origin = meta.get("origin")
    detail = _DETAIL.get(origin or "")
    keys = ["origin", detail, "from_store"]
    return {k: meta[k] for k in keys if k is not None and meta.get(k) not in (None, "")}


def _rank(item: dict[str, Any]) -> tuple:
    prov = item["provenance"]
    origin = prov.get("origin")
    place = PRECEDENCE.index(origin) if origin in PRECEDENCE else len(PRECEDENCE)
    return (place, item["relation"], str(prov.get("relation_doc") or prov.get("field") or ""), item["direction"], str(prov.get("from_store") or ""))
