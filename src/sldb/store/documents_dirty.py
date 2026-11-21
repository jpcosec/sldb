"""Per-model, per-namespace dirty tracking for `documents_hash`'s `note`/`forget` (PLAN 15
capa 8): one baseline per consumer ("semantic", "sections", ...), so one namespace's catch-up
(`clear`) never erases what another still needs — split out of documents_hash.py to keep
both files under this repo's clean-code line limit."""

from __future__ import annotations

from pathlib import Path

from sldb.store import documents_dirty_persist as persist

_DIRTY: dict[tuple[str, str, str], set[str]] = {}
_LOADED: set[str] = set()
_NAMESPACES = ("semantic", "sections", "edges")


def _load(s_path: Path) -> None:
    if (key := str(s_path)) not in _LOADED:
        _LOADED.add(key)
        for k, v in persist.load(s_path).items():
            _DIRTY.setdefault(k, v)


def mark(s_path: Path, model_name: str, name: str) -> None:
    _load(s_path)
    keys = [k for ns in _NAMESPACES if (k := (str(s_path), model_name, ns)) in _DIRTY]
    for k in keys:
        _DIRTY[k].add(name)
    if keys:
        persist.save(s_path, _DIRTY)


def invalidate(s_path: Path, model_name: str) -> None:
    _load(s_path)
    for ns in _NAMESPACES:
        _DIRTY.pop((str(s_path), model_name, ns), None)
    persist.save(s_path, _DIRTY)


def clear_all() -> None:
    for key in {k[0] for k in _DIRTY} | _LOADED:
        persist.delete(Path(key))
    _DIRTY.clear()
    _LOADED.clear()


def names(s_path: Path, model_name: str, namespace: str) -> set[str] | None:
    _load(s_path)
    known = _DIRTY.get((str(s_path), model_name, namespace))
    return None if known is None else set(known)


def clear(s_path: Path, model_name: str, namespace: str) -> None:
    _load(s_path)
    _DIRTY[(str(s_path), model_name, namespace)] = set()
    persist.save(s_path, _DIRTY)
