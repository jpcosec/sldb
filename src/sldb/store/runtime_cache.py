"""Caches for the runtime documents of a store, keyed by its signature (sldb.store.
runtime_cache_signature: hash_a, every model's hash_b, and the current operation's document
leaf sweep — see that module for the hand-edit guarantee PLAN 15 capa 6 changed). Two levels
in memory, the whole store and each document; a third on disk (runtime_cache_disk) spares a
new process the extraction. Cached documents are shared objects: a caller that mutates a
payload copies it first.

A document's key is `(store path, *leaf, model's hash_b, store name, model name)`. The model's
hash_b is the store's per-model record of its chain (kept by sldb.store.documents_hash, the
value `signature()` signs the store with): a payload is what the current model contract
extracts from the text, so when that chain moves the old payload must not win — even when the
leaf, and the markdown with it, did not move. The store path used to be missing: two stores
holding the same relative path with the same text under the same model name
shared one cached object — with the first store's `store_path` in it. `leaf_of` is where the
leaf sits inside the key, for the disk cache, which is already one file per store.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, Callable

from sldb.store import documents_hash
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
    """One document by its store, its leaf: (path, hash_c[, mtime, size]), and the model's
    hash_b — the same value the store's signature signs with, so a contract that moved
    invalidates the entry (in memory and on disk) even when the leaf did not."""
    leaf = _leaf(root, entry)
    key = (str(s_path), *leaf, documents_hash.hash_b_of(s_path, m_name), s_name, m_name)
    hit = _DOCS.get(key)
    if hit is None or hit.model_type is not model_type:
        hit = _remember(key, disk.from_disk(s_path, s_name, m_name, entry, leaf_of(key), model_type) or loader())
    return _with_entry(key, hit, entry) if hit is not None else None


def _remember(key: tuple, loaded: Any) -> Any:
    if loaded is not None:
        _DOCS[key] = loaded
        if disk.disk_key(leaf_of(key), loaded.model_name) not in disk.entries(loaded.store_path):
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


def leaf_of(key: tuple) -> tuple:
    """The document leaf inside a runtime cache key: what the disk cache keys on — the file
    state (path, hash_c[, mtime, size]) plus the model's hash_b, so a contract that moved
    misses the disk cache too."""
    return key[1:-2]


def payload_of(rel_path: str, hash_c: str, model_type: type) -> dict | None:
    """The extracted payload of this text under this model class, as the cache knows it now.

    Matched on the class itself, not on its name: a payload is what a class extracts from a
    text, and two classes called `Spec` in two modules extract different things. Matching the
    name let `hash_d` — which is persisted — be computed from another class's payload.
    """
    for key, doc in _DOCS.items():
        if key[1:3] == (rel_path, hash_c) and doc.model_type is model_type:
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
