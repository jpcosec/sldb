"""How two nodes are connected — the question the one-hop index could never answer."""

from __future__ import annotations

import networkx as nx

from sldb.store.graph.analysis.nx_graph import to_networkx


def path_between(index, source: str, target: str, relations: object = None, directed: bool = False) -> list[str] | None:
    """The shortest chain of nodes from `source` to `target`, or None when there is none.

    Undirected by default: `a implements b` connects the two whichever end you start from.
    """
    graph = _view(index, relations, directed)
    if source not in graph or target not in graph:
        return None
    try:
        return nx.shortest_path(graph, source, target)
    except nx.NetworkXNoPath:
        return None


def paths_between(index, source: str, target: str, relations: object = None, cutoff: int | None = None, limit: int = 10) -> list[list[str]]:
    """Up to `limit` distinct chains between the two nodes, shortest first, at most `cutoff` hops."""
    graph = _view(index, relations, directed=False)
    if source not in graph or target not in graph:
        return []
    found = nx.all_simple_paths(graph, source, target, cutoff=cutoff)
    return sorted(_take(found, limit), key=len)


def _view(index, relations: object, directed: bool):
    graph = to_networkx(index, relations)
    return graph if directed else graph.to_undirected(as_view=True)


def _take(paths, limit: int) -> list[list[str]]:
    out: list[list[str]] = []
    for path in paths:
        out.append(list(path))
        if len(out) >= limit:
            break
    return out
