"""The store's Merkle tree as one public value (spec 14 C10/D6).

``store_hash`` is the root; ``models`` maps each model to its ``model_hash``;
``documents`` keys ``"Model:name"`` to the document's raw-text (``source_hash``) and
extracted-fields (``content_hash``) hashes. Read through the existing index caches,
composed from the document shards: no document is re-extracted.
"""

from __future__ import annotations

from pathlib import Path

from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.layout import project_root
from sldb.store.models import DocumentHashes, ModelsIndex, StoreFingerprint


def store_fingerprint(store_path: Path) -> StoreFingerprint:
    """The whole tree: the root, every model hash, and every document's two hashes."""
    root = project_root(store_path)
    index = load_store_index(store_path)
    models: dict[str, str] = {}
    documents: dict[str, DocumentHashes] = {}
    for entry in index.models:
        m_idx = load_models_index(root / entry.models_index)
        models[entry.name] = m_idx.model_hash
        documents.update(_document_hashes(m_idx, entry.name, root))
    return StoreFingerprint(store_hash=index.store_hash, models=models, documents=documents)


def _document_hashes(m_idx: ModelsIndex, model_name: str, root: Path) -> dict[str, DocumentHashes]:
    index = load_documents_index(root / m_idx.documents_index)
    return {f"{model_name}:{d.name}": DocumentHashes(source_hash=d.source_hash, content_hash=d.content_hash) for d in index.documents}
