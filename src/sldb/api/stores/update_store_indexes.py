"""Refresh a store's indexes after its Markdown documents were edited outside sldb."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.stores.index_commit import commit_index_updates
from sldb.api.stores.index_refresh import _process_models
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_location import StoreLocation
from sldb.api.stores.store_update_report import StoreUpdateReport
from sldb.store.io import load_store_index


def update_store_indexes(store: str | Path | None, pythonpath: str | None = None, wait: bool = False) -> StoreUpdateReport:
    """Rehash changed documents, save model indexes and rebuild the derived indexes.

    Args:
        store: The store to refresh (path, alias, or None to discover it).
        pythonpath: Import root for the store's model modules.
        wait: Wait for the store lock instead of failing when another writer holds it.

    Returns:
        What was refreshed and which models or documents had to be skipped.
    """
    return StoreIndexRefresh(open_store(store), pythonpath)(wait)


class StoreIndexRefresh:
    """One refresh pass: accumulates skipped models/documents and the indexes to save."""

    def __init__(self, location: StoreLocation, pythonpath: str | None) -> None:
        """Prepare a refresh of the store at `location`, importing models from `pythonpath`."""
        self.location, self.pythonpath = location, pythonpath
        self.skipped_models: list[str] = []
        self.skipped_documents: list[str] = []
        self.pending: list[tuple[Any, Any, Any]] = []
        self.changed: dict[str, list[Any]] = {}

    def __call__(self, wait: bool) -> StoreUpdateReport:
        """Rehash, commit under the store lock (waiting for it if asked) and report."""
        sp, root = self.location.store_path, self.location.project_root
        idx = load_store_index(sp)
        _process_models(idx, root, self.pythonpath, self.skipped_models, self.skipped_documents, self.pending, self.changed)
        sem, sec = commit_index_updates(sp, root, idx, self.pending, self.changed, self.pythonpath, wait)
        return StoreUpdateReport(store_path=sp, skipped_models=self.skipped_models, skipped_documents=self.skipped_documents, semantic_index=sem, sections_index=sec)
