"""Whether a relation is really the DAG it claims to be.

`semantic_parent` is documented as a DAG and `extends` as an inheritance tree, but nothing ever
checked it. A cycle here is not a curiosity: it makes the semantic closure and the model load
order undefined.
"""

from __future__ import annotations

import networkx as nx

from sldb.store.graph.analysis.nx_graph import collapsed


def cycles(index, relations: object = None, limit: int = 10) -> list[list[str]]:
    """Up to `limit` cycles in the relations walked, shortest first; empty when it is a DAG."""
    graph = collapsed(index, relations)
    return sorted(_take(nx.simple_cycles(graph), limit), key=len)


def is_acyclic(index, relations: object = None) -> bool:
    """Whether the relations walked form a DAG."""
    return nx.is_directed_acyclic_graph(collapsed(index, relations))


def _take(found, limit: int) -> list[list[str]]:
    out: list[list[str]] = []
    for cycle in found:
        out.append(list(cycle))
        if len(out) >= limit:
            break
    return out
