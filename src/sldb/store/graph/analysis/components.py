"""What hangs together and what hangs alone.

A document nobody relates to and that relates to nobody is invisible to every walk. Counting
those, and the islands that never reach the main body of the store, is how you see the shape of
what has actually been asserted.

Here `node_types` restricts the **graph**, not the answer, and that is deliberate: "which specs
hang together" is a question about the subgraph the specs induce. `central` and `similar_to` go
the other way, because there the rest of the graph is what produces the number.
"""

from __future__ import annotations

import networkx as nx

from sldb.store.graph.analysis.nx_graph import to_networkx


def components(index, relations: object = None, node_types: object = None) -> list[list[str]]:
    """The weakly connected components, largest first, each sorted; isolated nodes included."""
    graph = to_networkx(index, relations, node_types)
    found = nx.weakly_connected_components(graph)
    return sorted((sorted(group) for group in found), key=lambda g: (-len(g), g[0]))


def islands(index, relations: object = None, node_types: object = None) -> list[list[str]]:
    """Every component but the largest: what never reaches the main body of the store."""
    return components(index, relations, node_types)[1:]


def isolated(index, relations: object = None, node_types: object = None) -> list[str]:
    """Nodes with no edge at all in the relations walked."""
    graph = to_networkx(index, relations, node_types)
    return sorted(n for n in graph.nodes if graph.degree(n) == 0)
