"""Neighborhood traversal over the edge index's _out/_in maps."""

from __future__ import annotations

from collections import deque


def collect_neighborhood_by_direction(index, starting_nodes: set[str], depth: int, direction: str) -> set[str]:
    """Collect nodes within `depth` hops and `direction` from the starting nodes."""
    visited: set[str] = set()
    queue = deque((node_id, 0) for node_id in starting_nodes)
    while queue:
        node_id, level = queue.popleft()
        if level >= depth:
            continue
        _enqueue_neighbors(index, node_id, direction, level, starting_nodes, visited, queue)
    return visited


def collect_neighborhood(index, starting_nodes: list[str], depth: int) -> set[str]:
    """The neighborhood including the seed nodes."""
    return collect_neighborhood_by_direction(index, set(starting_nodes), depth, "both") | set(starting_nodes)


def neighbors(index, node_id: str, direction: str) -> set[str]:
    """The node's neighbors on the requested side."""
    if direction == "incoming":
        return {e.source for e in index.edges_to(node_id)}
    if direction == "outgoing":
        return {e.target for e in index.edges_from(node_id)}
    return {e.source for e in index.edges_to(node_id)} | {e.target for e in index.edges_from(node_id)}


def _enqueue_neighbors(index, node_id: str, direction: str, level: int, starting_nodes: set[str], visited: set[str], queue) -> None:
    for neighbor in neighbors(index, node_id, direction):
        if neighbor in visited or neighbor in starting_nodes:
            continue
        visited.add(neighbor)
        queue.append((neighbor, level + 1))
