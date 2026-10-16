"""Every file a registered model owns in its store: its two indexes and its derived shards."""

from __future__ import annotations

import shutil
from pathlib import Path

from sldb.store import documents_hash
from sldb.store.io import invalidate_index_cache
from sldb.store.io.shards import invalidate_shard_cache
from sldb.store.layout import documents_shards_dir, edges_model_shard_path, edges_shards_dir, sections_index_relpath, sections_shards_dir, semantic_shards_dir

_SHARD_DIRS = (documents_shards_dir, sections_shards_dir, semantic_shards_dir, edges_shards_dir)


def drop_model_files(sp: Path, root: Path, name: str, models_index: str, documents_index: str) -> None:
    """Delete the model's indexes and shard directories; the caller holds the store lock."""
    for path in (root / models_index, root / documents_index, root / sections_index_relpath(sp, name), edges_model_shard_path(sp, name)):
        path.unlink(missing_ok=True)
    for shard_dir in _SHARD_DIRS:
        shutil.rmtree(shard_dir(sp, name), ignore_errors=True)
    invalidate_shard_cache()
    invalidate_index_cache()
    documents_hash.invalidate(sp, name)
