"""The documents a store tracks, read from its indexes alone.

No model class is imported and no payload extracted, so the documents of a linked store can be
listed or checked even when its models do not import from the caller's Python path.
"""

from __future__ import annotations

from pathlib import Path

from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.layout import project_root


def indexed_documents(store_path: Path) -> list[dict[str, str]]:
    """`{name, model, path}` of every tracked document, models in name order.

    Args:
        store_path: The store's `.sldb` directory.
    """
    root = project_root(store_path)
    docs: list[dict[str, str]] = []
    for entry in sorted(load_store_index(store_path).models, key=lambda item: item.name):
        index = load_documents_index(root / load_models_index(root / entry.models_index).documents_index)
        docs.extend({"name": d.name, "model": entry.name, "path": d.path} for d in index.documents)
    return docs
