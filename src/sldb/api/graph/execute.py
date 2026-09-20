"""Run structured queries and read nodes from a store's edge index."""

from __future__ import annotations

from typing import Iterable

from sldb.api.edges.edge_reading import load_edge_index
from sldb.store.graph.executor import execute_query as _execute
from sldb.store.graph.language import StructuredQuery
from sldb.store.graph.node_view import GraphNode


def execute_query(store, query: StructuredQuery, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> list[GraphNode]:
    """Execute a StructuredQuery over the store's edge index; returns matching nodes."""
    return _execute(load_edge_index(store, include_linked, exclude_tags), query)


def graph_get(store, node_id: str, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> GraphNode | None:
    """One node by id, with its edges; None when the index has no such node."""
    index = load_edge_index(store, include_linked, exclude_tags)
    node = index.node(node_id)
    if node is None:
        return None
    return GraphNode(id=node.id, node_type=node.node_type, semantics=node.semantics, facets=node.facets, edges=index.edges_from(node.id))


def graph_list(store, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> list[str]:
    """All node ids of the store's edge index, sorted."""
    return sorted(load_edge_index(store, include_linked, exclude_tags).nodes)
