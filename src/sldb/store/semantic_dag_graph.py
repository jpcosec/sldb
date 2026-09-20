"""The semantic DAG as a graph, which is what it always was.

A tag's dotted name is a path: `type.knowledge.anchor` serializes `type -> knowledge -> anchor`.
Until now the `se.` address space matched those strings with `startswith`, so the
`semantic_parent` edges the store keeps had no reader at all — delete the DAG and not one answer
changed. These walks read it.

Every edge in the DAG is still derived from a name today, so walking the graph and matching the
prefix agree. What changes is that a parent which is *not* a prefix becomes visible: the DAG file
has always been able to hold one, and nothing could see it.
"""

from __future__ import annotations

import networkx as nx


def dag_graph(dag) -> nx.DiGraph:
    """The DAG as `child -> parent` edges, the direction the tags declare."""
    graph = nx.DiGraph()
    graph.add_nodes_from(node.id for node in dag.nodes)
    graph.add_edges_from((node.id, parent) for node in dag.nodes for parent in node.parents)
    return graph


def children(dag, tag: str) -> list[str]:
    """The tags that declare `tag` as a parent, sorted."""
    graph = dag_graph(dag)
    return sorted(graph.predecessors(tag)) if tag in graph else []


def under(dag, tag: str) -> list[str]:
    """Every tag below `tag`, at any depth. Edges point at parents, so this is `ancestors`."""
    graph = dag_graph(dag)
    return sorted(nx.ancestors(graph, tag)) if tag in graph else []


def roots(dag) -> list[str]:
    """The tags with no parent: the tops of the DAG."""
    graph = dag_graph(dag)
    return sorted(node for node in graph if graph.out_degree(node) == 0)


def relative(tag: str, prefix: str) -> str:
    """How a child reads under its parent: the trailing segment, or the whole id when it is not
    a prefix of the child — which is what a parent declared by hand looks like."""
    return tag[len(prefix) + 1 :] if prefix and tag.startswith(f"{prefix}.") else tag
