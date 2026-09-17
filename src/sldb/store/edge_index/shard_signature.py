"""The state of a store's edges shards, cheaply: shards are written by rename, so a write,
a new shard or a pruned one moves the mtime of the directory it lives in. One stat per model
directory (not per document) says whether a composed index is still what the shards say."""

from __future__ import annotations

import os
from pathlib import Path

from sldb.store.layout import edges_shards_root, edges_store_shard_path, store_index_path


_REBUILDS: dict[str, int] = {}


def note_rebuild(store_path: Path) -> None:
    """This process just rewrote shards of that store: two writes inside one mtime tick must
    still read as two states."""
    _REBUILDS[str(store_path.resolve())] = _REBUILDS.get(str(store_path.resolve()), 0) + 1


def shards_signature(store_path: Path) -> tuple:
    """(rebuilds seen here, store index, store shard, edges root, every model shard and dir)."""
    root = edges_shards_root(store_path)
    heads = (_REBUILDS.get(str(store_path.resolve()), 0),) + tuple(_stat(p) for p in (store_index_path(store_path), edges_store_shard_path(store_path), root))
    return heads + tuple(_entries(root))


def _entries(root: Path) -> list[tuple]:
    try:
        with os.scandir(root) as found:
            return sorted((entry.name, *_stat(Path(entry.path))) for entry in found)
    except OSError:
        return []


def _stat(path: Path) -> tuple:
    try:
        st = path.stat()
        return (st.st_mtime_ns, st.st_size)
    except OSError:
        return (0, 0)
