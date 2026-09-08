"""Caches for the runtime documents of a store, keyed by the store's hash chain. hash_a
covers the models layer, each model's hash_b covers its documents, each document's hash_c
covers its text; every write through sldb moves the chain from the leaf up. So a query
descends only where a hash moved: the store index (one stat), the model indexes, and the
documents whose hash_c changed. One concession to Markdown edited by hand: the leaves are
also stat-ed (mtime and size, microseconds per file, no reads) so an edit made behind
sldb's back is seen before `stores update` moves its hash. A store that is only written
through sldb can set SLDB_TRUST_CHAIN=1 and skip that sweep. Two levels in memory, the
whole store and each document; a third on disk (runtime_cache_disk) spares a new process
the extraction. Cached documents are shared objects: a caller that mutates a payload
copies it first."""

from __future__ import annotations

import os
from dataclasses import replace
from pathlib import Path
from typing import Any, Callable

from sldb.store import runtime_cache_disk as disk
from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.layout import project_root

_STORES: dict[tuple, tuple[tuple, list]] = {}
_DOCS: dict[tuple, Any] = {}


def trust_chain() -> bool:
    return os.environ.get("SLDB_TRUST_CHAIN", "") not in ("", "0")


def _leaf(root: Path, entry: Any) -> tuple:
    """A document's place in the chain, plus its file state unless the chain is trusted."""
    if trust_chain():
        return (entry.path, entry.hash_c)
    try:
        st = (root / entry.path).stat()
        return (entry.path, entry.hash_c, st.st_mtime_ns, st.st_size)
    except OSError:
        return (entry.path, entry.hash_c, 0, 0)


def signature(s_path: Path) -> tuple:
    """hash_a, every model's hash_b, and (unless trusted) the state of every document file."""
    root = project_root(s_path)
    idx = load_store_index(s_path)
    parts: list = [idx.hash_a]
    for m in idx.models:
        m_idx = load_models_index(root / m.models_index)
        parts.append((m.name, m_idx.hash_b))
        if not trust_chain():
            parts.extend(_leaf(root, d) for d in load_documents_index(root / m_idx.documents_index).documents)
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
    """Drop the cached documents of one store, or of every store."""
    if store_path is None:
        _STORES.clear(); _DOCS.clear(); disk.clear()
        return
    for key in [k for k in _STORES if k[0] == str(store_path)]:
        del _STORES[key]
