"""Structured query execution over the edge index's _out/_in maps."""

from __future__ import annotations

from collections import deque

from sldb.store.graph.edge_filter import filtered_edges
from sldb.store.exceptions import SLDBGraphArgumentError
from sldb.store.graph.payload_match import filters_hold, unprojected_fields
from sldb.store.graph.node_view import GraphNode


def execute_query(index, query) -> list[GraphNode]:
    """Run a StructuredQuery against an edge index; returns matching nodes. Every condition is
    evaluated by the predicate language (`payload_match`). A `payload` filter reads the
    projection the shards hold (nothing is re-extracted); one naming a field no model projects
    is rejected (SLDBGraphArgumentError naming the field)."""
    _check_payload_fields(index, query.filters)
    matches: list[GraphNode] = []
    for node_id in candidate_ids(index, query.scope):
        node = index.nodes[node_id]
        if filters_hold(node, query.filters):
            matches.append(_node_view(index, node, query.relations))
    return matches


def _check_payload_fields(index, filters) -> None:
    missing = unprojected_fields(getattr(index, "payload_fields", {}), filters)
    if missing:
        raise SLDBGraphArgumentError(f"payload filter on {', '.join(repr(f) for f in missing)}: not projected into the graph (a dict or a list of non-scalars, outside the model's __indexed__, or not a field of any model).")


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
