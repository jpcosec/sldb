"""Bring a store's edge index current."""

from __future__ import annotations

from pathlib import Path

from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.stores.open_store import open_store
from sldb.store.edge_index.compose import compose_edge_index
from sldb.store.edge_index.edge_rebuild_report import EdgeRebuildReport
from sldb.store.edge_rebuild import rebuild_edges_indexes
from sldb.store.io import store_lock
from sldb.store.section_rebuild import rebuild_sections_indexes
from sldb.store.semantic import rebuild_semantic_indexes


def rebuild_edges(store: str | Path | None, pythonpath: str | None = None, wait: bool = False) -> EdgeRebuildReport:
    """Rebuild what moved in the edge index (after the semantic and sections indexes it reads).

    Only shards whose document `hash_c` moved are rewritten; on a current store this writes
    nothing. When the index reports stale documents (a shard deleted by hand, a store that
    predates the index) every shard is compared instead of trusting the caches. It reads the hashes the store has recorded: for files edited outside sldb, run
    `update_store_indexes` instead (it rehashes, then rebuilds this index too).

    Args:
        store: The store (path, alias, or None to discover it). Linked stores keep their own index.
        pythonpath: Directory to import the store's model modules from.
        wait: Wait for the store lock instead of failing when it is held.

    Returns:
        What was walked, written and reused.
    """
    location = open_store(store)
    with store_lock(location.store_path, wait=wait):
        rebuild_semantic_indexes(location.store_path, location.project_root, resolve_model_ref, pythonpath)
        rebuild_sections_indexes(location.store_path, location.project_root, resolve_model_ref, pythonpath)
        full = bool(compose_edge_index(location.store_path, include_linked=False).stale)
        return rebuild_edges_indexes(location.store_path, location.project_root, resolve_model_ref, pythonpath, full=full)
