"""Per-model, per-namespace dirty tracking for `documents_hash`'s `note`/`forget` (PLAN 15
capa 8): one baseline per consumer ("semantic", "sections", ...), so one namespace's catch-up
(`clear`) never erases what another still needs — split out of documents_hash.py to keep
both files under this repo's clean-code line limit."""

from __future__ import annotations

from pathlib import Path

_DIRTY: dict[tuple[str, str, str], set[str]] = {}
_NAMESPACES = ("semantic", "sections", "edges")


def mark(s_path: Path, model_name: str, name: str) -> None:
    for ns in _NAMESPACES:
        if (known := _DIRTY.get((str(s_path), model_name, ns))) is not None:
            known.add(name)


def invalidate(s_path: Path, model_name: str) -> None:
    for ns in _NAMESPACES:
        _DIRTY.pop((str(s_path), model_name, ns), None)


def clear_all() -> None:
    _DIRTY.clear()


def names(s_path: Path, model_name: str, namespace: str) -> set[str] | None:
    known = _DIRTY.get((str(s_path), model_name, namespace))
    return None if known is None else set(known)


def clear(s_path: Path, model_name: str, namespace: str) -> None:
    _DIRTY[(str(s_path), model_name, namespace)] = set()
