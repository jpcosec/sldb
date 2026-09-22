"""Derived results per model, keyed by the model's place in the hash chain: hash_b covers
the model's documents (path, hash_c, hash_d), so a model whose key is unchanged is not
walked again by a rebuild. In memory and on disk under the user's cache dir
(sldb.store.user_cache), so a new process skips the same models. Derived; safe to delete."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sldb.store import user_cache

_MEM: dict[str, dict] = {}


def _file(s_path: Path) -> Path | None:
    return user_cache.built_cache_file(s_path)


def _all(s_path: Path) -> dict:
    key = str(s_path)
    if key not in _MEM:
        try:
            path = _file(s_path)
            _MEM[key] = json.loads(path.read_text(encoding="utf-8")) if path else {}
        except (OSError, ValueError):
            _MEM[key] = {}
    return _MEM[key]


def model_key(m_idx: Any) -> str:
    """hash_b plus what the models index records about the class: version and semantics."""
    return f"{m_idx.hash_b}|{m_idx.version}|{','.join(m_idx.semantics or [])}"


def get(s_path: Path, kind: str, model: str, key: str) -> Any:
    entry = _all(s_path).get(kind, {}).get(model)
    return entry["value"] if entry is not None and entry.get("key") == key else None


def get_stale(s_path: Path, kind: str, model: str) -> Any:
    """The last value cached for `model`, regardless of whether its key still matches: a
    rebuild whose key moved (one document's hash_c changed the model's hash_b) still finds
    here the per-document work it does not need to redo (PLAN 15 M2)."""
    entry = _all(s_path).get(kind, {}).get(model)
    return entry["value"] if entry is not None else None


def put(s_path: Path, kind: str, model: str, key: str, value: Any) -> None:
    _all(s_path).setdefault(kind, {})[model] = {"key": key, "value": value}
    try:
        path = _file(s_path)
        if path is None:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(_all(s_path), ensure_ascii=False), encoding="utf-8")
    except (OSError, TypeError, ValueError):
        pass


def clear() -> None:
    _MEM.clear()
