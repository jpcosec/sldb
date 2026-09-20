"""Whole-graph analysis of a store: the questions that need more than one hop.

Each of these loads the store's edge index and hands it to `sldb.store.graph.analysis`. As
there, `relations=None` means the authored relations — the ones somebody asserted — because the
derived spine makes every document a neighbour of every other one.
"""

from __future__ import annotations

from typing import Iterable

from sldb.api.edges.edge_reading import load_edge_index
from sldb.store.graph import analysis


def graph_path(store, source: str, target: str, relations: object = None, directed: bool = False, **index) -> list[str] | None:
    """The shortest chain of nodes connecting two nodes, or None."""
    return analysis.path_between(_index(store, index), source, target, relations, directed)


def graph_paths(store, source: str, target: str, relations: object = None, cutoff: int | None = None, limit: int = 10, **index) -> list[list[str]]:
    """Up to `limit` distinct chains between two nodes, shortest first."""
    return analysis.paths_between(_index(store, index), source, target, relations, cutoff, limit)


def graph_cycles(store, relations: object = None, limit: int = 10, **index) -> list[list[str]]:
    """Cycles in the relations walked; empty when they form a DAG."""
    return analysis.cycles(_index(store, index), relations, limit)


def graph_order(store, relations: object = None, **index) -> list[str]:
    """Every node in dependency order; raises `SLDBGraphCycleError` when not a DAG."""
    return analysis.topological_order(_index(store, index), relations)


def graph_layers(store, relations: object = None, **index) -> list[list[str]]:
    """The dependency order as levels, each depending only on earlier ones."""
    return analysis.layers(_index(store, index), relations)


def graph_components(store, relations: object = None, node_types: object = None, **index) -> list[list[str]]:
    """What hangs together, largest group first."""
    return analysis.components(_index(store, index), relations, node_types)


def graph_islands(store, relations: object = None, node_types: object = None, **index) -> list[list[str]]:
    """Every group but the largest: what never reaches the main body of the store."""
    return analysis.islands(_index(store, index), relations, node_types)


def graph_isolated(store, relations: object = None, node_types: object = None, **index) -> list[str]:
    """Nodes with no edge at all in the relations walked."""
    return analysis.isolated(_index(store, index), relations, node_types)


def graph_central(store, kind: str = "pagerank", relations: object = None, node_types: object = None, limit: int = 20, **index) -> list[tuple[str, float]]:
    """The nodes the rest of the store leans on, with their score."""
    return analysis.central(_index(store, index), kind, relations, node_types, limit)


def graph_similar(store, node_id: str, relations: object = ("tagged_as",), limit: int = 10, node_types: object = None, **index) -> list[tuple[str, int]]:
    """Nodes sharing the most targets with this one: what resembles it, and how much."""
    return analysis.similar_to(_index(store, index), node_id, relations, limit, node_types)


def _index(store, options: dict):
    linked: bool = options.pop("include_linked", True)
    tags: Iterable[str] = options.pop("exclude_tags", ())
    if options:
        raise TypeError(f"Unexpected arguments: {', '.join(sorted(options))}")
    return load_edge_index(store, linked, tags)
