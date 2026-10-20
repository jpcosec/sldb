"""Caches for the runtime documents of a store, keyed by its signature (sldb.store.
runtime_cache_signature: store_hash, every model's model_hash, and the current operation's document
leaf sweep — see that module for the hand-edit guarantee PLAN 15 capa 6 changed). Two levels
in memory, the whole store and each document; a third on disk (runtime_cache_disk) spares a
new process the extraction. Cached documents are shared objects: a caller that mutates a
payload copies it first.

A document's key is `(store path, *leaf, the model's contract_hash, store name, model name)`: a
payload is what the current contract extracts from the text, so a contract that moved must not
be served the old payload — even when the leaf, and the markdown with it, did not move. The
store path used to be missing: two stores holding the same relative path with the same text
under the same model name shared one cached object, with the first store's `store_path` in it.
`leaf_of` is where the leaf sits inside the key, for the disk cache (one file per store).
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, Callable

from sldb.store import documents_hash  # noqa: F401 - re-exported for existing importers
from sldb.store import runtime_cache_disk as disk
from sldb.store.hashing import hash_model_contract
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
    """One document by its store, its leaf: (path, source_hash[, mtime, size]), and the contract
    of the class being extracted with, so a moved contract invalidates the entry (in memory and
    on disk) even when the leaf did not. The contract is hashed from `model_type` itself, not
    read from the models index: the index only learns of a contract change when something
    writes, and a pure read (new field on the class, same Markdown) must not be served a payload
    extracted under the old contract — the standing bug where a new field stayed invisible."""
    leaf = _leaf(root, entry)
    key = (str(s_path), *leaf, hash_model_contract(model_type), s_name, m_name)
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
    """The name, the tags and the two index hashes come from the index and can change without
    the text changing; the cached object is stamped with the entry's current values."""
    tags = list(entry.semantic_tags)
    current = (hit.name, hit.semantic_tags, hit.source_hash, hit.content_hash, hit.provenance)
    fresh = (entry.name, tags, entry.source_hash, entry.content_hash, entry.provenance)
    if current == fresh:
        return hit
    hit = replace(hit, name=entry.name, semantic_tags=tags, source_hash=entry.source_hash, content_hash=entry.content_hash, provenance=entry.provenance)
    _DOCS[key] = hit
    return hit


def leaf_of(key: tuple) -> tuple:
    """The document leaf inside a runtime cache key: what the disk cache keys on — the file
    state (path, source_hash[, mtime, size]) plus the model's model_hash, so a contract that moved
    misses the disk cache too."""
    return key[1:-2]


def payload_of(rel_path: str, hash_c: str, model_type: type) -> dict | None:
    """The extracted payload of this text under this model class, as the cache knows it now.

    Matched on the class itself, not on its name: a payload is what a class extracts from a
    text, and two classes called `Spec` in two modules extract different things. Matching the
    name let `content_hash` — which is persisted — be computed from another class's payload.
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
