from __future__ import annotations

from pathlib import Path

from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_sections_index,
    load_semantic_dag,
    load_semantic_index,
    load_store_index,
    save_documents_index,
    save_models_index,
    save_sections_index,
    save_semantic_dag,
    save_semantic_index,
    save_store_index,
)
from sldb.store.layout import (
    documents_index_relpath,
    models_index_relpath,
    sections_index_relpath,
    store_index_path,
)


def _migrate_model(m_entry, p_root) -> bool:
    m_idx = load_models_index(p_root / m_entry.models_index)
    n_m_rel, n_d_rel, n_s_rel = models_index_relpath(m_entry.name), documents_index_relpath(m_entry.name), sections_index_relpath(m_entry.name)
    save_documents_index(p_root / n_d_rel, load_documents_index(p_root / m_idx.documents_index))
    if m_idx.sections_index:
        save_sections_index(p_root / n_s_rel, load_sections_index(p_root / m_idx.sections_index))
    changed = m_idx.documents_index != n_d_rel or m_entry.models_index != n_m_rel
    m_idx.documents_index, m_idx.sections_index = n_d_rel, n_s_rel if m_idx.sections_index else ""
    save_models_index(p_root / n_m_rel, m_idx)
    m_entry.models_index = n_m_rel
    return changed

def _model_canonical(m_entry, p_root: Path) -> bool:
    if m_entry.models_index != models_index_relpath(m_entry.name) or not (p_root / m_entry.models_index).exists():
        return False
    m_idx = load_models_index(p_root / m_entry.models_index)
    if m_idx.documents_index != documents_index_relpath(m_entry.name) or not (p_root / m_idx.documents_index).exists():
        return False
    return not m_idx.sections_index or (m_idx.sections_index == sections_index_relpath(m_entry.name) and (p_root / m_idx.sections_index).exists())

def _already_canonical(store_index, p_root: Path) -> bool:
    """True when every model index already sits at its canonical path and points at canonical
    document and section indexes: nothing to migrate, and nothing to rewrite."""
    return all(_model_canonical(m_entry, p_root) for m_entry in store_index.models)


def migrate_store_layout(store_path: Path, project_root: Path) -> bool:
    store_index = load_store_index(store_path)
    if store_index_path(store_path).exists() and _already_canonical(store_index, project_root):
        return False   # the common case: an up-to-date store is not rewritten on every context
    changed = not store_index_path(store_path).exists()
    for m_entry in store_index.models:
        if _migrate_model(m_entry, project_root): changed = True
    save_semantic_dag(store_path, load_semantic_dag(store_path))
    save_semantic_index(store_path, load_semantic_index(store_path))
    if changed: save_store_index(store_path, store_index)
    return changed
