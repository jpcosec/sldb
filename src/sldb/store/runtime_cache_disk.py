"""The cache file of extracted payloads: what a process extracted, keyed by the document's
leaf key (path, hash_c and, unless the chain is trusted, mtime and size) plus the model's
hash_b, and the model name — so the next process does not extract a store it has already
seen, and a payload extracted under a contract that has since moved is not reused.

Derived and safe to delete. It lives in the user's cache dir (sldb.store.user_cache), never
inside the store, so a read never writes into a store that may be tracked."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sldb.store import user_cache

_DISK: dict[str, dict] = {}
_DIRTY: set[str] = set()


def cache_file(s_path: Path) -> Path | None:
    return user_cache.extracted_cache_file(s_path)


def disk_key(leaf: tuple, m_name: str) -> str:
    return "|".join(str(x) for x in leaf) + f"|{m_name}"


def entries(s_path: Path) -> dict:
    key = str(s_path)
    if key not in _DISK:
        try:
            path = cache_file(s_path)
            _DISK[key] = json.loads(path.read_text(encoding="utf-8")) if path else {}
        except (OSError, ValueError):
            _DISK[key] = {}
    return _DISK[key]


def mark_dirty(s_path: Path) -> None:
    _DIRTY.add(str(s_path))


def from_disk(s_path: Path, s_name: str, m_name: str, entry: Any, leaf: tuple, model_type: type) -> Any:
    """A document whose payload the cache file already holds: no extraction. `leaf` is the
    key material `runtime_cache.leaf_of` hands over — the document's file state plus the
    model's hash_b — so a contract change misses here exactly like in memory."""
    from sldb.store.query_engine.models import RuntimeDocument
    hit = entries(s_path).get(disk_key(leaf, m_name))
    if hit is None:
        return None
    return RuntimeDocument(store_name=s_name, store_path=s_path, model_name=m_name, model_type=model_type, name=entry.name, path=entry.path, payload=hit["payload"], semantic_tags=list(entry.semantic_tags))


def flush(s_path: Path, docs: dict[tuple, Any]) -> None:
    """Write the file from every document of this store in memory: a full load just happened,
    so that is the whole store, and stale signatures fall away."""
    if str(s_path) not in _DIRTY:
        return
    _DIRTY.discard(str(s_path))
    fresh = {disk_key(k[1:-2], d.model_name): {"payload": d.payload} for k, d in docs.items() if k[0] == str(s_path)}
    _write(s_path, fresh)


def _write(s_path: Path, fresh: dict) -> None:
    try:
        path = cache_file(s_path)
        if path is None:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(fresh, ensure_ascii=False), encoding="utf-8")
        _DISK[str(s_path)] = fresh
    except (OSError, TypeError, ValueError):
        pass


def forget(s_path: Path, predicate: Any) -> int:
    """Drop every cache entry whose key matches, and rewrite the file. Returns how many.

    For deletions: a document that no longer exists keeps its entry here until some
    process does a full load and `flush` rewrites the whole file.
    """
    current = entries(s_path)
    stale = [key for key in current if predicate(key)]
    if stale:
        for key in stale:
            current.pop(key)
        _write(s_path, current)
    return len(stale)


def clear() -> None:
    _DISK.clear()
    _DIRTY.clear()
