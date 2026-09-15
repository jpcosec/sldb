"""Bringing one model's sections shards current (PLAN 15 capa 5): skipped whole when the
model's hash_b has not moved; otherwise every document's shard synced (`section_doc_
contribution.sync_doc_shard`) and shards of documents no longer tracked pruned. The
markdown parsing itself stays in section_rebuild.py; this is the per-model plumbing around
it, split out to keep both files under this project's own line-count rule."""

from __future__ import annotations

import logging
from pathlib import Path

from sldb.store.io import load_documents_index, load_models_index, save_models_index
from sldb.store.io.shards import prune_shards
from sldb.store.layout import sections_index_relpath, sections_shards_dir
from sldb.store.section_doc_contribution import sync_doc_shard

logger = logging.getLogger(__name__)


def process_model_sections(m_entry, root, report, store_path: Path | None, process_doc_sections) -> None:
    from sldb.store import built_cache

    m_idx = load_models_index(root / m_entry.models_index)
    key = built_cache.model_key(m_idx)
    if store_path and built_cache.get(store_path, "sections_shards", m_entry.name, key) is not None:
        return
    current = _sync_model_sections(store_path, m_entry, m_idx, root, report, process_doc_sections)
    _mark_has_sections(m_entry, m_idx, root, current)
    if store_path:
        built_cache.put(store_path, "sections_shards", m_entry.name, key, True)


def _mark_has_sections(m_entry, m_idx, root, current: set[str]) -> None:
    if current and not m_idx.sections_index:
        m_idx.sections_index = sections_index_relpath(m_entry.name)
        save_models_index(root / m_entry.models_index, m_idx)


def _sync_model_sections(store_path, m_entry, m_idx, root, report, process_doc_sections) -> set[str]:
    current: set[str] = set()
    for doc in load_documents_index(root / m_idx.documents_index).documents:
        if _sync_one_section(store_path, doc, m_entry, root, report, process_doc_sections):
            current.add(doc.name)
    if store_path:
        prune_shards(sections_shards_dir(store_path, m_entry.name), current)
    return current


def _sync_one_section(store_path, doc, m_entry, root, report, process_doc_sections) -> bool:
    d_path = root / doc.path
    if not d_path.exists():
        _missing_doc(doc, d_path, report)
        return False
    sync_doc_shard(store_path, doc, d_path, m_entry, report, process_doc_sections)
    return True


def _missing_doc(doc, d_path, report) -> None:
    report.docs_skipped_missing += 1
    report.verbose.append(f"sections: {doc.name} — missing file {d_path}")
    logger.warning(f"Sections rebuild: doc '{doc.name}' missing at {d_path}")
