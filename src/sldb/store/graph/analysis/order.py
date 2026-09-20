"""A relation in dependency order: what has to come before what."""

from __future__ import annotations

import networkx as nx

from sldb.core.exceptions import SLDBGraphCycleError
from sldb.store.graph.analysis.cycles import cycles
from sldb.store.graph.analysis.nx_graph import collapsed


def topological_order(index, relations: object = None) -> list[str]:
    """Every node ordered so a node comes after everything it points at.

    Raises `SLDBGraphCycleError` with the offending cycle when the relation is not a DAG.
    """
    graph = collapsed(index, relations)
    if not nx.is_directed_acyclic_graph(graph):
        raise SLDBGraphCycleError(cycles(index, relations, limit=1)[0])
    return list(reversed(list(nx.topological_sort(graph))))


def layers(index, relations: object = None) -> list[list[str]]:
    """The same order as levels: everything in a level depends only on earlier levels."""
    graph = collapsed(index, relations)
    if not nx.is_directed_acyclic_graph(graph):
        raise SLDBGraphCycleError(cycles(index, relations, limit=1)[0])
    return [sorted(level) for level in nx.topological_generations(graph.reverse(copy=False))]
