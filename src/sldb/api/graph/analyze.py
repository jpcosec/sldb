"""Whole-graph analysis of a store: the questions that need more than one hop.

Each function composes the store's edge index, hands it to a `GraphBackend` with `load`, and
asks for one operation with `analyze`. Today the backend is networkx; the commands and the
library see no difference. `relations=None` still means the authored relations — the ones
somebody asserted — because the derived spine makes every document a neighbour of every other
one.

A caller may pass `backend=` to use another implementation (the tests' spy, or a future
engine). Without it, the store's `.sldb/store.yaml` decides, with networkx as the default.
"""

from __future__ import annotations

from typing import Any, Iterable

from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBGraphArgumentError
from sldb.store.graph.backend import GraphBackend, backend_for


def graph_path(store, source: str, target: str, relations: object = None, directed: bool = False, backend: GraphBackend | None = None, **index) -> list[str] | None:
    """The shortest chain of nodes connecting two nodes, or None."""
    return _run(store, "path", {"source": source, "target": target, "relations": relations, "directed": directed}, index, backend)


def graph_paths(store, source: str, target: str, relations: object = None, cutoff: int | None = None, limit: int = 10, backend: GraphBackend | None = None, **index) -> list[list[str]]:
    """Up to `limit` distinct chains between two nodes, shortest first."""
    return _run(store, "paths", {"source": source, "target": target, "relations": relations, "cutoff": cutoff, "limit": limit}, index, backend)


def graph_cycles(store, relations: object = None, limit: int = 10, backend: GraphBackend | None = None, **index) -> list[list[str]]:
    """Cycles in the relations walked; empty when they form a DAG."""
    return _run(store, "cycles", {"relations": relations, "limit": limit}, index, backend)


def graph_order(store, relations: object = None, backend: GraphBackend | None = None, **index) -> list[str]:
    """Every node in dependency order; raises `SLDBGraphCycleError` when not a DAG."""
    return _run(store, "order", {"relations": relations}, index, backend)


def graph_layers(store, relations: object = None, backend: GraphBackend | None = None, **index) -> list[list[str]]:
    """The dependency order as levels, each depending only on earlier ones."""
    return _run(store, "layers", {"relations": relations}, index, backend)


def graph_components(store, relations: object = None, node_types: object = None, backend: GraphBackend | None = None, **index) -> list[list[str]]:
    """What hangs together, largest group first."""
    return _run(store, "components", {"relations": relations, "node_types": node_types}, index, backend)


def graph_islands(store, relations: object = None, node_types: object = None, backend: GraphBackend | None = None, **index) -> list[list[str]]:
    """Every group but the largest: what never reaches the main body of the store."""
    return _run(store, "islands", {"relations": relations, "node_types": node_types}, index, backend)


def graph_isolated(store, relations: object = None, node_types: object = None, backend: GraphBackend | None = None, **index) -> list[str]:
    """Nodes with no edge at all in the relations walked."""
    return _run(store, "isolated", {"relations": relations, "node_types": node_types}, index, backend)


def graph_central(store, kind: str = "pagerank", relations: object = None, node_types: object = None, limit: int = 20, backend: GraphBackend | None = None, **index) -> list[tuple[str, float]]:
    """The nodes the rest of the store leans on, with their score."""
    return _run(store, "central", {"kind": kind, "relations": relations, "node_types": node_types, "limit": limit}, index, backend)


def graph_similar(store, node_id: str, relations: object = ("tagged_as",), limit: int = 10, node_types: object = None, backend: GraphBackend | None = None, **index) -> list[tuple[str, int]]:
    """Nodes sharing the most targets with this one: what resembles it, and how much."""
    return _run(store, "similar", {"node_id": node_id, "relations": relations, "limit": limit, "node_types": node_types}, index, backend)


def _run(store: Any, op: str, arguments: dict[str, Any], options: dict[str, Any], backend: GraphBackend | None) -> Any:
    """Compose the index, load it into the backend, and ask for the operation."""
    index = _index(store, options)
    engine = backend if backend is not None else backend_for(open_store(store, mode="readonly").store_path)
    engine.load(index, None)
    return engine.analyze(op, **arguments)


def _index(store, options: dict):
    linked: bool = options.pop("include_linked", True)
    tags: Iterable[str] = options.pop("exclude_tags", ())
    if options:
        raise SLDBGraphArgumentError(f"Unexpected arguments: {', '.join(sorted(options))}")
    return load_edge_index(store, linked, tags)
