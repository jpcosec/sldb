"""The candidate rows of `select_documents` kept on disk between processes (H11b):
`<cache>/document_rows/<id>.json` in the calling store's `.sldb_cache`. A new process that finds
every store where the file saw it reads plain JSON (never executed) instead of parsing each
document shard again. The file holds the key it was built under; any difference is a miss, so a
written, added or removed document, a moved model index or another sldb version reads the shards
as before. The key is stats only: it never reads the shards it spares."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from sldb.store.edge_index.cache_keys import edge_shard_version
from sldb.store.io import load_models_index, load_store_index
from sldb.store.layout import cache_dir, core_dir, project_root, store_index_path

FORMAT = "1"


def rows_key(stores: list[tuple[Path, str | None]]) -> dict[str, Any]:
    """What the rows depend on: per store, its index, each model's index (its stat and roster hash: a written
    document moves the hash even inside one clock tick) and the mtime of each model's document-shard directory (a write is a rename)."""
    key = {"format": FORMAT, "edges": edge_shard_version(), "stores": [[str(p), a, _state(p)] for p, a in stores]}
    return json.loads(json.dumps(key))  # as a file reads it back: lists, not tuples


def load_rows(calling: Path, key: dict[str, Any]) -> list[dict[str, Any]] | None:
    """The rows saved under exactly this key; None on a miss, a corrupt file or another version."""
    try:
        saved = json.loads(_file(calling).read_text(encoding="utf-8"))
        rows = saved["rows"]
        return rows if saved["key"] == key and isinstance(rows, list) else None
    except (OSError, ValueError, KeyError, TypeError):
        return None


def save_rows(calling: Path, key: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    """Keep the rows for the next process; a store that cannot be written is not an error."""
    path = _file(calling)
    tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps({"key": key, "rows": rows}), encoding="utf-8")
        os.replace(tmp, path)
    except (OSError, TypeError, ValueError):
        tmp.unlink(missing_ok=True)


def _file(calling: Path) -> Path:
    return cache_dir(calling) / "document_rows" / f"{hashlib.sha256(str(calling.resolve()).encode()).hexdigest()[:16]}.json"


def _state(store_path: Path) -> list:
    root = project_root(store_path)
    models = [[m.name, _stat(root / m.models_index), load_models_index(root / m.models_index).roster_hash] for m in load_store_index(store_path).models]
    return [_stat(store_index_path(store_path)), models, _documents_dirs(store_path)]


def _documents_dirs(store_path: Path) -> list:
    try:
        with os.scandir(core_dir(store_path) / "documents") as found:
            return sorted([e.name, *_stat(Path(e.path))] for e in found)
    except OSError:
        return []


def _stat(path: Path) -> list[int]:
    try:
        st = path.stat()
        return [st.st_mtime_ns, st.st_size]
    except OSError:
        return [0, 0]
