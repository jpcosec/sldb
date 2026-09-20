"""Structured query execution over the edge index's _out/_in maps."""

from __future__ import annotations

from collections import deque

from sldb.store.graph.edge_filter import filtered_edges
from sldb.store.graph.facet_match import matches_filters
from sldb.store.graph.node_view import GraphNode


def execute_query(index, query) -> list[GraphNode]:
    """Run a StructuredQuery against an edge index; returns matching nodes."""
    matches: list[GraphNode] = []
    for node_id in candidate_ids(index, query.scope):
        node = index.nodes[node_id]
        if matches_filters(node, query.filters):
            matches.append(_node_view(index, node, query.relations))
    return matches


def candidate_ids(index, scope) -> list[str]:
    """The node ids the scope admits, sorted for determinism."""
    if scope is None:
        return sorted(index.nodes)
    if scope.descendant_of:
        return sorted(descendants(index, scope.descendant_of))
    if scope.ancestor_of:
        return sorted(ancestors(index, scope.ancestor_of))
    if scope.node_id_prefix:
        return sorted(n for n in index.nodes if n.startswith(scope.node_id_prefix))
    return sorted(index.nodes)


def descendants(index, root: str) -> set[str]:
    """Nodes reachable from `root` following outgoing edges, excluding `root` itself."""
    visited = {root}
    queue = deque([root])
    while queue:
        for edge in index.edges_from(queue.popleft()):
            if edge.target not in visited:
                visited.add(edge.target)
                queue.append(edge.target)
    visited.discard(root)
    return visited


def ancestors(index, root: str) -> set[str]:
    """Nodes that reach `root` following incoming edges, excluding `root` itself."""
    visited = {root}
    queue = deque([root])
    while queue:
        for edge in index.edges_to(queue.popleft()):
            if edge.source not in visited:
                visited.add(edge.source)
                queue.append(edge.source)
    visited.discard(root)
    return visited


def _node_view(index, node, relation_filters) -> GraphNode:
    return GraphNode(id=node.id, node_type=node.node_type, semantics=node.semantics, facets=node.facets, edges=filtered_edges(index, node.id, relation_filters))
