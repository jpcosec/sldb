"""Caches for the runtime documents of a store, keyed by the store's hash chain. hash_a
covers the models layer, each model's hash_b covers its documents, each document's hash_c
covers its text; every write through sldb moves the chain from the leaf up. So a query
does not stat or read documents to know whether its cache holds: it reads the store index
(one stat) and the model indexes, and descends only where a hash moved. Two levels in
memory, the whole store and each document; a third on disk (runtime_cache_disk) spares a
new process the extraction. A document edited behind sldb's back is not seen until
`stores update` rehashes it, which is the contract of the chain. Cached documents are
shared objects: a caller that mutates a payload copies it first."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, Callable

from sldb.store import runtime_cache_disk as disk
from sldb.store.io import load_models_index, load_store_index
from sldb.store.layout import project_root

_STORES: dict[tuple, tuple[tuple, list]] = {}
_DOCS: dict[tuple, Any] = {}


def signature(s_path: Path) -> tuple:
    """hash_a and every model's hash_b: the store's place in its hash chain."""
    root = project_root(s_path)
    idx = load_store_index(s_path)
    return (idx.hash_a, tuple((m.name, load_models_index(root / m.models_index).hash_b) for m in idx.models))


def cached_store(s_path: Path, s_name: str, pythonpath: str | None, loader: Callable[[], list]) -> list:
    key = (str(s_path), s_name, pythonpath)
    sig = signature(s_path)
    hit = _STORES.get(key)
    if hit is not None and hit[0] == sig:
        return hit[1]
    docs = loader()
    _STORES[key] = (sig, docs)
    disk.flush(s_path, _DOCS)
    return docs


def cached_document(entry: Any, s_path: Path, s_name: str, m_name: str, model_type: type, loader: Callable[[], Any]) -> Any:
    """One document by (path, hash_c, model): the leaf of the chain."""
    key = (entry.path, entry.hash_c, s_name, m_name)
    hit = _DOCS.get(key)
    if hit is None or hit.model_type is not model_type:
        hit = _remember(key, disk.from_disk(s_path, s_name, m_name, entry, model_type) or loader())
    return _with_entry(key, hit, entry) if hit is not None else None


def _remember(key: tuple, loaded: Any) -> Any:
    if loaded is not None:
        _DOCS[key] = loaded
        if disk.disk_key(loaded.path, key[1], loaded.model_name) not in disk.entries(loaded.store_path):
            disk.mark_dirty(loaded.store_path)
    return loaded


def _with_entry(key: tuple, hit: Any, entry: Any) -> Any:
    """The name and the tags come from the index and can change without the text changing."""
    tags = list(entry.semantic_tags)
    if hit.name == entry.name and hit.semantic_tags == tags:
        return hit
    hit = replace(hit, name=entry.name, semantic_tags=tags)
    _DOCS[key] = hit
    return hit


def payload_of(rel_path: str, hash_c: str, m_name: str) -> dict | None:
    """The extracted payload of a document as the cache knows it now, or None."""
    for key, doc in _DOCS.items():
        if key[0] == rel_path and key[1] == hash_c and key[3] == m_name:
            return doc.payload
    return None


def invalidate_runtime_cache(store_path: Path | None = None) -> None:
    """Drop the cached documents of one store, or of every store."""
    if store_path is None:
        _STORES.clear(); _DOCS.clear(); disk.clear()
        return
    for key in [k for k in _STORES if k[0] == str(store_path)]:
        del _STORES[key]
