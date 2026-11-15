"""Edges and neighbourhoods of a document or node."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import sldb.api as api
from sldb.api import graph
from sldb.mcp.addresses import node_or_document, relation_type_address
from sldb.mcp.paging import page
from sldb.mcp.read.miss import missing

#: The directions `collect_neighborhood_by_direction` understands; any other value would be
#: read by SLDB as "both", so it is refused here instead.
NEIGHBORHOOD_DIRECTIONS = ("outgoing", "incoming", "both")
#: One-hop neighbours: `edges_from` (outgoing) or `edges_to` (incoming).
NEIGHBOR_DIRECTIONS = ("outgoing", "incoming")


def undeclared(store_path: Path, address: str, relation: str | None) -> tuple[str, str, str] | None:
    """What a graph question names that the store does not declare: (signal class, name, why), or None."""
    if api.edge_node(store_path, address) is None:
        return "unknown_document", address, f"the edge index has no node {address}"
    if relation and api.edge_node(store_path, relation_type_address(relation)) is None:
        return "unknown_relation", relation, f"the edge index declares no relation type {relation!r}; list_relation_types names the ones it does"
    return None


def edge_page(store_path: Path, address: str, direction: str, relation: str | None, offset: int, limit: int) -> dict[str, Any]:
    """The edges leaving or reaching `address`, as one page."""
    read = api.edges_from if direction == "outgoing" else api.edges_to
    edges = [e.model_dump(mode="json") for e in read(store_path, address, relation)]
    return page(edges, offset, limit, None if edges else f"{address} has no {direction} edge" + (f" of relation {relation!r}" if relation else ""))


def neighbors(store_path: Path, node: str, direction: str, relation: str | None, offset: int, limit: int) -> dict[str, Any]:
    """The edges leaving (`outgoing`, `edges_from`) or reaching (`incoming`, `edges_to`) a
    document (`[alias:]Model:name`) or any node id (`sldb://...`), optionally of one relation type."""
    if direction not in NEIGHBOR_DIRECTIONS:
        raise ValueError(f"direction must be one of {NEIGHBOR_DIRECTIONS}, not {direction!r}")
    address = node_or_document(node)
    head, gap = {"node": address, "direction": direction, "relation": relation}, undeclared(store_path, address, relation)
    if gap:
        return missing(gap[0], gap[1], {**head, **page([], offset, limit, gap[2])})
    return {**head, **edge_page(store_path, address, direction, relation, offset, limit)}


def neighborhood(store_path: Path, node: str, direction: str, depth: int, offset: int, limit: int) -> dict[str, Any]:
    """The node ids within `depth` hops of `node` in one direction, seeds excluded. Every
    relation type of the index is walked; no relation filter applies per hop."""
    if direction not in NEIGHBORHOOD_DIRECTIONS:
        raise ValueError(f"direction must be one of {NEIGHBORHOOD_DIRECTIONS}, not {direction!r}")
    if depth < 1:
        raise ValueError(f"depth must be >= 1, not {depth}")
    address = node_or_document(node)
    head, gap = {"node": address, "direction": direction, "depth": depth}, undeclared(store_path, address, None)
    if gap:
        return missing(gap[0], gap[1], {**head, **page([], offset, limit, gap[2])})
    nodes = sorted(graph.collect_neighborhood_by_direction(store_path, {address}, depth, direction))
    return {**head, **page(nodes, offset, limit, None if nodes else f"no node lies within {depth} {direction} hop(s) of {address}")}
