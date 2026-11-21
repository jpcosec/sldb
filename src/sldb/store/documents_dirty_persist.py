"""The dirty-document sets of `documents_dirty`, kept in `<store>/../.sldb_cache/documents_dirty.json`
so an incremental update in a new process processes only what changed. Regenerable and untracked:
a missing, corrupt, or stale (different store signature) file reads as "no baseline" and the caller
compares every document, silently. Writes are atomic (tmp + os.replace) under the store lock."""

from __future__ import annotations

import json
import os
from pathlib import Path

from sldb.store.io import store_lock
from sldb.store.layout import cache_dir

FILE_NAME = "documents_dirty.json"
Key = tuple[str, str, str]


def _file(s_path: Path) -> Path:
    return cache_dir(s_path) / FILE_NAME


def _signature(s_path: Path) -> str | None:
    from sldb.store.runtime_cache_signature import signature

    try:
        return json.dumps(list(signature(s_path)), default=str)
    except Exception:
        return None


def delete(s_path: Path) -> None:
    try:
        with store_lock(s_path, wait=True):
            _file(s_path).unlink(missing_ok=True)
    except Exception:
        pass


def _entries(raw: object) -> list | None:
    ok = isinstance(raw, list) and all(
        isinstance(e, list) and len(e) == 3 and isinstance(e[0], str) and isinstance(e[1], str)
        and isinstance(e[2], list) and all(isinstance(n, str) for n in e[2])
        for e in raw
    )
    return raw if ok else None


def _read(s_path: Path) -> list | None:
    """The file's entries when it parses, has the right shape and carries this store's signature."""
    try:
        data = json.loads(_file(s_path).read_text(encoding="utf-8"))
        entries = _entries(data["entries"])
        return entries if data["signature"] == _signature(s_path) else None
    except (ValueError, KeyError, TypeError):
        return None


def load(s_path: Path) -> dict[Key, set[str]]:
    """What the file holds for this store; {} when absent, corrupt or written under another signature."""
    if not _file(s_path).exists():
        return {}
    entries = _read(s_path)
    if entries is None:
        delete(s_path)
        return {}
    return {(str(s_path), m, ns): set(names) for m, ns, names in entries}


def _write(s_path: Path, sig: str, entries: list) -> None:
    with store_lock(s_path, wait=True):
        path = _file(s_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_name(f"{FILE_NAME}.{os.getpid()}.tmp")
        tmp.write_text(json.dumps({"signature": sig, "entries": entries}), encoding="utf-8")
        os.replace(tmp, path)


def save(s_path: Path, dirty: dict[Key, set[str]]) -> None:
    """Rewrite the file with every entry this process holds for the store; silent on any failure."""
    try:
        sig = _signature(s_path)
        if sig is not None and s_path.exists():
            _write(s_path, sig, [[m, ns, sorted(v)] for (p, m, ns), v in sorted(dirty.items()) if p == str(s_path)])
    except Exception:
        pass
