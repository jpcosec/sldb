"""Whether a store tracks a document under a given name.

Shared by ``/document`` and ``/document/segments`` so both return the same 404
for the same reason. Lifted out of ``document_routes`` when the segments route
needed the identical check; the walk over the store's indexes is unchanged.
"""

from __future__ import annotations

from pathlib import Path

from sldb.store.io import load_documents_index, load_models_index, load_store_index


def is_tracked(store_path: Path, root: Path, name: str) -> bool:
    """Whether any model in the store tracks a document called ``name``.

    Args:
        store_path: Path of the ``.sldb`` store.
        root: Root the store's index paths are relative to.
        name: The document name to look for.

    Returns:
        True when some model's document index lists that name.
    """
    index = load_store_index(store_path)
    for model in index.models:
        m_idx = load_models_index(root / model.models_index)
        d_idx = load_documents_index(root / m_idx.documents_index)
        if any(doc.name == name for doc in d_idx.documents):
            return True
    return False
