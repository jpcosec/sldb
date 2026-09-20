"""Graph analysis over the edge index, on networkx.

The index answers one hop: who points at this, what does this point at. These are the questions
that need the whole graph — how two nodes connect, whether a relation is acyclic, what order it
imposes, what hangs alone, what the store leans on, what resembles what.

Every one of them takes the relations to walk and defaults to the **authored** ones, because the
derived spine (`has_document`, `has_section`...) makes any two documents neighbours and turns
every answer into a truism. See `relations`.
"""

from sldb.store.graph.analysis.centrality import KINDS, central
from sldb.store.graph.analysis.components import components, islands, isolated
from sldb.store.graph.analysis.cycles import cycles, is_acyclic
from sldb.store.graph.analysis.nx_graph import collapsed, to_networkx
from sldb.store.graph.analysis.order import layers, topological_order
from sldb.store.graph.analysis.paths import path_between, paths_between
from sldb.store.graph.analysis.relations import ALL, DERIVED, authored, present, resolve
from sldb.store.graph.analysis.similarity import of_types, similar_to

__all__ = [
    "ALL",
    "DERIVED",
    "KINDS",
    "authored",
    "central",
    "collapsed",
    "components",
    "cycles",
    "is_acyclic",
    "islands",
    "isolated",
    "of_types",
    "layers",
    "path_between",
    "paths_between",
    "present",
    "resolve",
    "similar_to",
    "to_networkx",
    "topological_order",
]
