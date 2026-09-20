"""What hangs together and what hangs alone.

A document nobody relates to and that relates to nobody is invisible to every walk. Counting
those, and the islands that never reach the main body of the store, is how you see the shape of
what has actually been asserted.

`node_types` means one thing for grouping and the other for `isolated`, and the difference is
the whole point of having both. For `components` and `islands` it restricts the **graph**:
"which specs hang together" is a question about the subgraph the specs induce. For `isolated` it
filters the **answer**: "which specs is nothing attached to" is about the whole graph — a spec
that only ever appears as the target of a surface is attached to plenty, and calling it isolated
because no other spec points at it would be a lie. `central` and `similar_to` filter the answer
for the same reason.
"""

from __future__ import annotations

import networkx as nx

from sldb.store.graph.analysis.nx_graph import to_networkx
from sldb.store.graph.analysis.similarity import of_types


def components(index, relations: object = None, node_types: object = None) -> list[list[str]]:
    """The weakly connected components, largest first, each sorted; isolated nodes included."""
    graph = to_networkx(index, relations, node_types)
    found = nx.weakly_connected_components(graph)
    return sorted((sorted(group) for group in found), key=lambda g: (-len(g), g[0]))


def islands(index, relations: object = None, node_types: object = None) -> list[list[str]]:
    """Every component but the largest: what never reaches the main body of the store."""
    return components(index, relations, node_types)[1:]


def isolated(index, relations: object = None, node_types: object = None) -> list[str]:
    """Nodes that no edge of the relations walked touches, of those classes if given.

    Measured on the whole graph, then filtered: a node attached to something of another class is
    not isolated.
    """
    graph = to_networkx(index, relations)
    alone = {n: 0 for n in graph.nodes if graph.degree(n) == 0}
    return sorted(of_types(index, alone, node_types))
