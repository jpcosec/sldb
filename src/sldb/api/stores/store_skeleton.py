"""Write the empty indexes of a new store and register it in the global catalog.

Moved here from `sldb.cli.commands.store_init`.
"""

from __future__ import annotations

from pathlib import Path

from sldb.store.catalog import register_project_store
from sldb.store.io import save_semantic_dag, save_semantic_index, save_store_index
from sldb.store.models import SemanticDAG, SemanticIndex, StoreIndex
from sldb.store.predicates import default_predicates
from sldb.store.resolver import global_store_path


def write_empty_store(store_path: Path) -> None:
    """Write a store index seeded with the default predicates, an empty DAG and semantic index.

    Args:
        store_path: The `.sldb` directory to create.
    """
    save_store_index(store_path, StoreIndex(predicates=default_predicates()))
    save_semantic_dag(store_path, SemanticDAG(equivalences={}))
    save_semantic_index(store_path, SemanticIndex())


def register_in_global_catalog(store_path: Path) -> None:
    """Record a project store in the global store, creating the global store when missing.

    Only stores under HOME are recorded (see `register_project_store`); the global store
    itself is never registered in itself.

    Args:
        store_path: The project's `.sldb` directory.
    """
    global_store = global_store_path().resolve()
    if store_path.resolve() == global_store:
        return
    if not global_store.exists():
        write_empty_store(global_store)
    register_project_store(store_path)
