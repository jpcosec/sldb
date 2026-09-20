"""Which nodes are load-bearing.

Not "which document is longest" but "which one does the rest of the store lean on". PageRank
over the authored relations answers what breaks if you delete something; betweenness answers
what is a bridge between parts that would otherwise not talk.

`node_types` filters the **answer**, not the graph it is computed on: a node is central because
of the whole graph around it, and deleting half the graph first would measure something else.
`components` does the opposite on purpose: see there.

Everything here is pure networkx except PageRank, whose networkx implementation is built on
scipy. A markdown library has no business dragging scipy into every install, so that one kind —
and only that one — asks for the `graph` extra, and says so instead of failing obscurely.
"""

from __future__ import annotations

import networkx as nx

from sldb.core.exceptions import SLDBError
from sldb.store.graph.analysis.nx_graph import collapsed
from sldb.store.graph.analysis.similarity import of_types

KINDS = ("pagerank", "betweenness", "degree", "in_degree", "out_degree")


def central(index, kind: str = "pagerank", relations: object = None, node_types: object = None, limit: int = 20) -> list[tuple[str, float]]:
    """The `limit` most central nodes with their score, highest first.

    `kind` is one of `KINDS`. Ties break by node id so the answer is stable.
    """
    if kind not in KINDS:
        raise ValueError(f"Unknown centrality {kind!r}; expected one of {', '.join(KINDS)}.")
    scores = of_types(index, _scores(collapsed(index, relations), kind), node_types)
    ranked = sorted(scores.items(), key=lambda pair: (-pair[1], pair[0]))
    return [(node, float(score)) for node, score in ranked[:limit]]


def _scores(graph, kind: str) -> dict:
    if kind == "pagerank":
        return _pagerank(graph) if graph.number_of_edges() else dict.fromkeys(graph, 0.0)
    if kind == "betweenness":
        return nx.betweenness_centrality(graph)
    return _degrees(graph, kind)


def _pagerank(graph) -> dict:
    try:
        return nx.pagerank(graph)
    except ImportError as missing:
        raise SLDBError(
            "PageRank is networkx-on-scipy, and sldb does not require scipy: install it with "
            "`pip install 'sldb[graph]'`, or ask for a centrality that does not need it "
            "(degree, in_degree, out_degree, betweenness)."
        ) from missing


def _degrees(graph, kind: str) -> dict:
    view = {"degree": graph.degree, "in_degree": graph.in_degree, "out_degree": graph.out_degree}[kind]
    return dict(view())
