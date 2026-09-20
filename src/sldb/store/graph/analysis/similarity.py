"""Which nodes resemble one another, by what they point at.

Two documents carrying the same tags, or implementing the same spec, are neighbours in a way no
edge between them records. This is the bipartite projection of the index: shared targets.

`node_types` filters the **answer**, not the graph it is computed on. Restricting the view first
would delete the very nodes the resemblance goes through — ask for documents only and every tag
disappears, so nothing resembles anything. `components` does the opposite on purpose: see there.
"""

from __future__ import annotations

from collections import Counter

from sldb.store.graph.analysis.nx_graph import to_networkx


def similar_to(index, node_id: str, relations: object = ("tagged_as",), limit: int = 10, node_types: object = None) -> list[tuple[str, int]]:
    """Nodes sharing the most targets with `node_id`, most shared first.

    Defaults to `tagged_as`: what else is tagged the way this is. Ties break by node id.
    """
    graph = to_networkx(index, relations)
    if node_id not in graph:
        return []
    shared = of_types(index, _shared_counts(graph, node_id), node_types)
    ranked = sorted(shared.items(), key=lambda pair: (-pair[1], pair[0]))
    return [(node, int(count)) for node, count in ranked[:limit]]


def of_types(index, scores: dict, node_types: object) -> dict:
    """Keep only the scores of nodes of those classes; all of them when none is asked for."""
    if node_types is None:
        return dict(scores)
    wanted = set(node_types)
    return {node: score for node, score in scores.items() if _type_of(index, node) in wanted}


def _type_of(index, node_id: str) -> str | None:
    record = index.nodes.get(node_id) or index.node(node_id)
    return record.node_type if record else None


def _shared_counts(graph, node_id: str) -> Counter:
    counts: Counter = Counter()
    for target in set(graph.successors(node_id)):
        for other in set(graph.predecessors(target)):
            if other != node_id:
                counts[other] += 1
    return counts
