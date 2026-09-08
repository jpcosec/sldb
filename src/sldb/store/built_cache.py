"""Derived results per model, keyed by the model's place in the hash chain: hash_b covers
the model's documents (path, hash_c, hash_d), so a model whose key is unchanged is not
walked again by a rebuild. In memory and in `.sldb/runtime/cache/built.json`, so a new
process skips the same models. Derived; safe to delete."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_MEM: dict[str, dict] = {}


def _file(s_path: Path) -> Path:
    return s_path / "runtime" / "cache" / "built.json"


def _all(s_path: Path) -> dict:
    key = str(s_path)
    if key not in _MEM:
        try:
            _MEM[key] = json.loads(_file(s_path).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            _MEM[key] = {}
    return _MEM[key]


def model_key(m_idx: Any) -> str:
    """hash_b plus what the models index records about the class: version and semantics."""
    return f"{m_idx.hash_b}|{m_idx.version}|{','.join(m_idx.semantics or [])}"


def get(s_path: Path, kind: str, model: str, key: str) -> Any:
    entry = _all(s_path).get(kind, {}).get(model)
    return entry["value"] if entry is not None and entry.get("key") == key else None


def put(s_path: Path, kind: str, model: str, key: str, value: Any) -> None:
    _all(s_path).setdefault(kind, {})[model] = {"key": key, "value": value}
    try:
        path = _file(s_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(_all(s_path), ensure_ascii=False), encoding="utf-8")
    except (OSError, TypeError, ValueError):
        pass


def clear() -> None:
    _MEM.clear()
