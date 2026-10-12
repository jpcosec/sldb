"""The documents a store tracks, as (name, absolute path)."""
from __future__ import annotations
from pathlib import Path
from sldb.store.io import load_documents_index, load_models_index, load_store_index

def tracked_documents(store_path: Path, root: Path) -> list[tuple[str, Path]]:
    docs = []
    for model in load_store_index(store_path).models:
        m_idx = load_models_index(root / model.models_index)
        d_idx = load_documents_index(root / m_idx.documents_index)
        docs += [(d.name, (root / d.path).resolve()) for d in d_idx.documents]
    return docs
