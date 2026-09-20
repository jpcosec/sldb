"""Neighborhood traversal over a store's edge index."""

from __future__ import annotations

from typing import Iterable

from sldb.api.edges.edge_reading import load_edge_index
from sldb.store.graph.neighborhood import collect_neighborhood as _collect
from sldb.store.graph.neighborhood import collect_neighborhood_by_direction as _collect_directed


def collect_neighborhood(store, starting_nodes: list[str], depth: int, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> set[str]:
    """The nodes within `depth` hops of the starting nodes, seeds included."""
    return _collect(load_edge_index(store, include_linked, exclude_tags), starting_nodes, depth)


def collect_neighborhood_by_direction(store, starting_nodes: set[str], depth: int, direction: str, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> set[str]:
    """The nodes within `depth` hops on one direction, seeds excluded."""
    return _collect_directed(load_edge_index(store, include_linked, exclude_tags), starting_nodes, depth, direction)
