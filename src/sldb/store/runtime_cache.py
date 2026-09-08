"""Caches for the runtime documents of a store, keyed by the state of the files they come
from. Loading a store means reading and extracting every tracked document, and a query
engine asks for that on every call; without a cache a session of a few queries reads the
store a few times over. Two levels in memory: the whole store, validated by the signature
of every file the load depends on (store index, model indexes, document indexes,
documents), and each document by its own path, mtime and size, so a reload after one
write extracts one document. A third level on disk (runtime_cache_disk) spares a new
process the extraction. Any write through sldb touches an index or a document, so the
next load sees a new signature. Cached documents are shared objects: a caller that
mutates a payload copies it first."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, Callable

from sldb.store import runtime_cache_disk as disk
from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.layout import project_root

_STORES: dict[tuple, tuple[tuple, list]] = {}
_DOCS: dict[tuple, Any] = {}


def _stat(path: Path) -> tuple:
    try:
        st = path.stat()
        return (str(path), st.st_mtime_ns, st.st_size)
    except OSError:
        return (str(path), 0, 0)


def signature(s_path: Path) -> tuple:
    """Every file a load of this store depends on, with its mtime and size."""
    root = project_root(s_path)
    parts = [_stat(s_path / "core" / "store_index.yaml")]
    for m in load_store_index(s_path).models:
        parts.append(_stat(root / m.models_index))
        m_idx = load_models_index(root / m.models_index)
        parts.append(_stat(root / m_idx.documents_index))
        parts.extend(_stat(root / d.path) for d in load_documents_index(root / m_idx.documents_index).documents)
    return tuple(parts)


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


def cached_document(d_path: Path, s_path: Path, s_name: str, m_name: str, entry: Any, model_type: type, loader: Callable[[], Any]) -> Any:
    sig = _stat(d_path)
    if sig[1] == 0:
        return None
    key = (*sig, s_name, m_name)
    hit = _DOCS.get(key)
    if hit is None or hit.model_type is not model_type:
        hit = _remember(key, disk.from_disk(s_path, s_name, m_name, entry, sig, model_type) or loader())
    return _with_entry(key, hit, entry) if hit is not None else None


def _remember(key: tuple, loaded: Any) -> Any:
    if loaded is not None:
        _DOCS[key] = loaded
        if disk.disk_key(loaded.path, key, loaded.model_name) not in disk.entries(loaded.store_path):
            disk.mark_dirty(loaded.store_path)
    return loaded


def _with_entry(key: tuple, hit: Any, entry: Any) -> Any:
    """The name and the tags come from the index and can change without the file changing."""
    tags = list(entry.semantic_tags)
    if hit.name == entry.name and hit.semantic_tags == tags:
        return hit
    hit = replace(hit, name=entry.name, semantic_tags=tags)
    _DOCS[key] = hit
    return hit


def payload_of(d_path: Path, m_name: str) -> dict | None:
    """The extracted payload of a document as the cache knows it now, or None."""
    sig = _stat(d_path)
    for key, doc in _DOCS.items():
        if key[:3] == sig and key[4] == m_name:
            return doc.payload
    return None


def invalidate_runtime_cache(store_path: Path | None = None) -> None:
    """Drop the cached documents of one store, or of every store."""
    if store_path is None:
        _STORES.clear(); _DOCS.clear(); disk.clear()
        return
    for key in [k for k in _STORES if k[0] == str(store_path)]:
        del _STORES[key]
