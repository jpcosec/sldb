"""Caches for the runtime documents of a store, keyed by its signature (sldb.store.
runtime_cache_signature: hash_a, every model's hash_b, and the current operation's document
leaf sweep — see that module for the hand-edit guarantee PLAN 15 capa 6 changed). Two levels
in memory, the whole store and each document; a third on disk (runtime_cache_disk) spares a
new process the extraction. Cached documents are shared objects: a caller that mutates a
payload copies it first."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, Callable

from sldb.store import runtime_cache_disk as disk
from sldb.store.runtime_cache_signature import (
    forget as _forget_signature,
    leaf as _leaf,
    new_operation,  # noqa: F401 - re-exported: get_store_context calls this
    signature,
    trust_chain,  # noqa: F401 - re-exported: tests set SLDB_TRUST_CHAIN and check this
)

_STORES: dict[tuple, tuple[tuple, list]] = {}
_DOCS: dict[tuple, Any] = {}


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


def cached_document(entry: Any, root: Path, s_path: Path, s_name: str, m_name: str, model_type: type, loader: Callable[[], Any]) -> Any:
    """One document by its leaf key: (path, hash_c[, mtime, size])."""
    leaf = _leaf(root, entry)
    key = (*leaf, s_name, m_name)
    hit = _DOCS.get(key)
    if hit is None or hit.model_type is not model_type:
        hit = _remember(key, disk.from_disk(s_path, s_name, m_name, entry, leaf, model_type) or loader())
    return _with_entry(key, hit, entry) if hit is not None else None


def _remember(key: tuple, loaded: Any) -> Any:
    if loaded is not None:
        _DOCS[key] = loaded
        if disk.disk_key(key[:-2], loaded.model_name) not in disk.entries(loaded.store_path):
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
        if key[0] == rel_path and key[1] == hash_c and key[-1] == m_name:
            return doc.payload
    return None


def invalidate_runtime_cache(store_path: Path | None = None) -> None:
    """Drop the cached documents of one store, or of every store; either way, a call to
    signature() for that store sweeps document leaves fresh again next time too."""
    if store_path is None:
        _STORES.clear(); _DOCS.clear(); disk.clear(); _forget_signature(None)
        return
    for key in [k for k in _STORES if k[0] == str(store_path)]:
        del _STORES[key]
    _forget_signature(store_path)
