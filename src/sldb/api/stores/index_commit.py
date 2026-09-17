"""Save refreshed model indexes and rebuild the derived store indexes under the store lock.

Moved here from `sldb.cli.commands.store_update`, which re-exports `_rebuild_indexes`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.store import documents_hash
from sldb.store.edge_rebuild import rebuild_edges_indexes
from sldb.store.io import save_documents_index, save_models_index, store_lock
from sldb.store.models.store_index import StoreIndex
from sldb.store.ops import cascade_hash_a
from sldb.store.section_rebuild import rebuild_sections_indexes
from sldb.store.semantic import RebuildReport, rebuild_semantic_indexes


def commit_index_updates(sp: Path, root: Path, idx: StoreIndex, pending: list[tuple[Any, Any, Any]], changed: dict[str, list[Any]], pythonpath: str | None, wait: bool) -> tuple[RebuildReport, RebuildReport]:
    """Persist every queued model's indexes, then rebuild semantic and section indexes.

    Args:
        sp: The store's `.sldb` directory.
        root: The store's project root.
        idx: The store index whose hash_a is recomputed at the end.
        pending: (model entry, models index, documents index) triples to save.
        changed: Documents whose hashes moved, by model name.
        pythonpath: Import root for the store's model modules.
        wait: Wait for the store lock instead of failing when it is held.

    Returns:
        The semantic and sections rebuild reports.
    """
    with store_lock(sp, wait=wait):
        for m_entry, m_idx, d_idx in pending:
            save_documents_index(root / m_idx.documents_index, d_idx)
            for doc in changed.get(m_entry.name, []):
                documents_hash.note(sp, m_entry.name, doc)  # the map now agrees with what was just saved
            m_idx.hash_b = documents_hash.hash_b_of(sp, m_entry.name)
            m_idx.documents_count = documents_hash.count_of(sp, m_entry.name)
            save_models_index(root / m_entry.models_index, m_idx)
        return _rebuild_indexes(sp, root, idx, pythonpath)


def _rebuild_indexes(sp: Path, root: Path, idx: StoreIndex, pypath: str | None) -> tuple[RebuildReport, RebuildReport]:
    """Rebuild the semantic, section and edge indexes and cascade the store hash."""
    sem_report = rebuild_semantic_indexes(sp, root, resolve_model_ref, pypath)
    sec_report = rebuild_sections_indexes(sp, root, resolve_model_ref, pypath)
    rebuild_edges_indexes(sp, root, resolve_model_ref, pypath)
    cascade_hash_a(sp, root, idx)
    return sem_report, sec_report
