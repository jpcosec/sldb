"""The cache file of extracted payloads, `.sldb/runtime/cache/extracted.json`: what a
process extracted, keyed by document path, hash_c and model, so the next process
does not extract a store it has already seen. Derived and safe to delete; a store's
.gitignore should list `.sldb/runtime/cache/`."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_DISK: dict[str, dict] = {}
_DIRTY: set[str] = set()


def cache_file(s_path: Path) -> Path:
    return s_path / "runtime" / "cache" / "extracted.json"


def disk_key(rel_path: str, hash_c: str, m_name: str) -> str:
    return f"{rel_path}|{hash_c}|{m_name}"


def entries(s_path: Path) -> dict:
    key = str(s_path)
    if key not in _DISK:
        try:
            _DISK[key] = json.loads(cache_file(s_path).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            _DISK[key] = {}
    return _DISK[key]


def mark_dirty(s_path: Path) -> None:
    _DIRTY.add(str(s_path))


def from_disk(s_path: Path, s_name: str, m_name: str, entry: Any, model_type: type) -> Any:
    """A document whose payload the cache file already holds: no extraction."""
    from sldb.store.query_engine.models import RuntimeDocument
    hit = entries(s_path).get(disk_key(entry.path, entry.hash_c, m_name))
    if hit is None:
        return None
    return RuntimeDocument(store_name=s_name, store_path=s_path, model_name=m_name, model_type=model_type, name=entry.name, path=entry.path, payload=hit["payload"], semantic_tags=list(entry.semantic_tags))


def flush(s_path: Path, docs: dict[tuple, Any]) -> None:
    """Write the file from every document of this store in memory: a full load just happened,
    so that is the whole store, and stale signatures fall away."""
    if str(s_path) not in _DIRTY:
        return
    _DIRTY.discard(str(s_path))
    fresh = {disk_key(d.path, k[1], d.model_name): {"payload": d.payload} for k, d in docs.items() if str(d.store_path) == str(s_path)}
    _write(s_path, fresh)


def _write(s_path: Path, fresh: dict) -> None:
    try:
        path = cache_file(s_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(fresh, ensure_ascii=False), encoding="utf-8")
        _DISK[str(s_path)] = fresh
    except (OSError, TypeError, ValueError):
        pass


def clear() -> None:
    _DISK.clear()
    _DIRTY.clear()
