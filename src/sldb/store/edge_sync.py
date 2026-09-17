"""Bringing one model's edges shards current (mirror of section_sync): skipped whole when the
model's cache key has not moved; otherwise the model's own shard is rebuilt, every dirty
document's shard synced (`edge_doc_contribution.sync_doc_shard`) and the shards of documents
no longer tracked pruned."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from sldb.store import built_cache, documents_hash
from sldb.store.edge_doc_contribution import sync_doc_shard
from sldb.store.edge_index.cache_keys import edge_cache_key, edge_shard_version
from sldb.store.edge_index.edge_rebuild_report import EdgeRebuildReport
from sldb.store.edge_index.model_contribution import build_model_edges
from sldb.store.io import load_models_index
from sldb.store.io.shards import prune_shards, save_edges_shard
from sldb.store.layout import edges_model_shard_path, edges_shards_dir

DocBuilder = Callable[[Any, Any, Any], Any]


def process_model_edges(m_entry, root: Path, report: EdgeRebuildReport, store_path: Path, model_type: Callable[[], Any], build_doc_edges: DocBuilder, full: bool = False) -> None:
    """One model's shards, current. `model_type` imports the class only if the model is walked;
    `build_doc_edges(m_entry, model_type, doc)` is edge_rebuild's own document builder; `full`
    compares every document's shard whatever the caches say."""
    m_idx = load_models_index(root / m_entry.models_index)
    key, model_shard = edge_cache_key(m_idx), edges_model_shard_path(store_path, m_entry.name)
    wiped = full or not model_shard.exists()  # no shards to trust: neither the cache key nor the dirty set
    if not wiped and built_cache.get(store_path, "edges_shards", m_entry.name, key) is not None:
        return
    report.models_walked += 1
    resolved = model_type()
    save_edges_shard(model_shard, build_model_edges(m_idx, resolved).model_copy(update={"edges_version": edge_shard_version()}))
    _sync_model_docs(store_path, m_entry, root, report, lambda doc: build_doc_edges(m_entry, resolved, doc), wiped)
    built_cache.put(store_path, "edges_shards", m_entry.name, key, True)


def _sync_model_docs(store_path: Path, m_entry, root: Path, report: EdgeRebuildReport, build_one, every: bool) -> None:
    """PLAN 15 capa 8, as sections does it: every document's file is cheaply checked to exist,
    but only one in the dirty set (or every one, with no trustworthy baseline) has its shard
    opened and compared."""
    entries = documents_hash.entries_of(store_path, m_entry.name)
    dirty = None if every else documents_hash.dirty_names(store_path, m_entry.name, "edges")
    current = {doc.name for doc in entries if _sync_one(store_path, doc, m_entry, root, report, build_one, dirty is None or doc.name in dirty)}
    prune_shards(edges_shards_dir(store_path, m_entry.name), current)
    documents_hash.clear_dirty(store_path, m_entry.name, "edges")


def _sync_one(store_path: Path, doc, m_entry, root: Path, report: EdgeRebuildReport, build_one, do_sync: bool) -> bool:
    if not (root / doc.path).exists():
        report.docs_skipped_missing += 1
        return False
    if do_sync:
        sync_doc_shard(store_path, doc, m_entry, report, build_one)
    return True
