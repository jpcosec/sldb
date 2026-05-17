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


def migrate_store_layout(store_path: Path, project_root: Path) -> bool:
    """Materialize legacy flat store metadata into core/runtime paths."""
    store_index = load_store_index(store_path)
    changed = not store_index_path(store_path).exists()

    for model_entry in store_index.models:
        current_model_rel = model_entry.models_index
        current_model_path = project_root / current_model_rel
        models_idx = load_models_index(current_model_path)

        new_model_rel = models_index_relpath(model_entry.name)
        new_docs_rel = documents_index_relpath(model_entry.name)
        new_sections_rel = sections_index_relpath(model_entry.name)

        docs_idx = load_documents_index(project_root / models_idx.documents_index)
        save_documents_index(project_root / new_docs_rel, docs_idx)

        if models_idx.sections_index:
            sections_idx = load_sections_index(project_root / models_idx.sections_index)
            save_sections_index(project_root / new_sections_rel, sections_idx)
            models_idx.sections_index = new_sections_rel

        if models_idx.documents_index != new_docs_rel:
            changed = True
        if current_model_rel != new_model_rel:
            changed = True

        models_idx.documents_index = new_docs_rel
        save_models_index(project_root / new_model_rel, models_idx)
        model_entry.models_index = new_model_rel

    save_semantic_dag(store_path, load_semantic_dag(store_path))
    save_semantic_index(store_path, load_semantic_index(store_path))

    if changed:
        save_store_index(store_path, store_index)

    return changed
