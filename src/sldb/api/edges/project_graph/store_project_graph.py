"""`sldb.api.project_graph(store)`: the project graph a store declares in its `store.yaml`."""

from __future__ import annotations

from pathlib import Path

from sldb.api.edges.project_graph.project_graph import ProjectGraph
from sldb.api.edges.project_graph.project_graph_config import ProjectGraphConfig
from sldb.api.edges.project_graph.project_graph_memo import memoized_project_graph
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_declaration import load_declaration
from sldb.core.exceptions import SLDBStoreError


def project_graph(store: str | Path | None = None) -> ProjectGraph:
    """The declared-edge graph of the project whose store declares `project_graph`.

    The configuration is read from `store.yaml` (`ProjectGraphConfig.from_mapping`), so it
    holds no callable; the graph is kept per process and rebuilt only when the shards, a file
    it read or a directory it walked moved (`project_graph_memo`).

    Args:
        store: The store (path, alias, or None to discover it); the project is its root.

    Returns:
        The project's graph: nodes, `edges_from`, `edges_to`, `missing_from`, `extraction`.

    Raises:
        SLDBStoreError: `store.yaml` declares no `project_graph`.
        ValueError: The declaration does not load (an unknown key, a value that is not data).
        FileNotFoundError: The store has no `store.yaml`.
    """
    store_path = open_store(store, mode="readonly").store_path
    return memoized_project_graph(store_path, declared_project_graph_config(store_path))


def declared_project_graph_config(store_path: Path) -> ProjectGraphConfig:
    """The `project_graph` of the store's declaration, loaded as data."""
    declared = load_declaration(store_path).project_graph
    if declared is None:
        raise SLDBStoreError(f"{store_path / 'store.yaml'} declares no project_graph")
    return ProjectGraphConfig.from_mapping(declared)
