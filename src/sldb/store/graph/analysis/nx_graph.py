"""The edge index as a networkx graph: the view every analysis in this package runs on.

Built on demand and never persisted — the index is the source of truth, this is a projection of
it. Nodes keep their class and semantics; every edge keys on its relation name, so a
`MultiDiGraph` holds two nodes related twice in two different ways without losing either.
"""

from __future__ import annotations

import networkx as nx

from sldb.store.graph.analysis.relations import resolve


def to_networkx(index, relations: object = None, node_types: object = None) -> nx.MultiDiGraph:
    """The index as a `MultiDiGraph`, restricted to some relations and node classes."""
    kept = resolve(index, relations)
    graph = nx.MultiDiGraph()
    for node in _nodes(index, node_types):
        graph.add_node(node.id, node_type=node.node_type, semantics=dict(node.semantics))
    for edge in index.edges:
        if edge.relation in kept and edge.source in graph and edge.target in graph:
            graph.add_edge(edge.source, edge.target, key=edge.relation, relation=edge.relation)
    return graph


def collapsed(index, relations: object = None, node_types: object = None) -> nx.DiGraph:
    """The same view as one edge per ordered pair: what the weighted algorithms need."""
    multi = to_networkx(index, relations, node_types)
    graph = nx.DiGraph()
    graph.add_nodes_from(multi.nodes(data=True))
    for source, target in set(multi.edges()):
        graph.add_edge(source, target, weight=multi.number_of_edges(source, target))
    return graph


def _nodes(index, node_types: object) -> list:
    if node_types is None:
        return list(index.nodes.values())
    wanted = set(node_types)
    return [n for n in index.nodes.values() if n.node_type in wanted]
