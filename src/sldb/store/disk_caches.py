"""The caches the store keeps on disk between processes, and how to forget them."""

from __future__ import annotations

from pathlib import Path

from sldb.store.layout import cache_dir

DISK_CACHE_KINDS = ("composed", "document_rows")


def drop_disk_caches(store_path: Path) -> None:
    """Forget what earlier processes kept on disk of the store's composed edge index and of its
    document rows (H11, H11b): the next read builds them again from the shards."""
    for kind in DISK_CACHE_KINDS:
        for path in (cache_dir(store_path) / kind).glob("*.json"):
            path.unlink(missing_ok=True)
