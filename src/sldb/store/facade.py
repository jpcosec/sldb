"""
Store facade for decoupling CLI from low-level store operations.
"""
from pathlib import Path
from typing import Any
from sldb.store.io import load_store_index, load_models_index, load_documents_index

def get_tracked_docs(model_name: str, store_path: Path, root: Path) -> list[tuple[str, str]]:
    m_entry = next((m for m in load_store_index(store_path).models if m.name == model_name), None)
    if not m_entry:
        from sldb.store.exceptions import SLDBError
        raise SLDBError(f"Model '{model_name}' not found.")
    d_idx = load_documents_index(root / load_models_index(root / m_entry.models_index).documents_index)
    return [
        (d.name, str(Path(d.path) if Path(d.path).is_absolute() else root / d.path))
        for d in d_idx.documents
    ]
