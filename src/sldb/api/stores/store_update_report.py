"""Outcome of refreshing a store's indexes, as returned by `update_store_indexes`."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from sldb.store.semantic import RebuildReport


class StoreUpdateReport(BaseModel):
    """What an index refresh did and what it had to skip."""

    store_path: Path = Field(description="The `.sldb` directory whose indexes were refreshed.")
    skipped_models: list[str] = Field(description="Registered models whose class could not be imported; their documents were not rehashed.")
    skipped_documents: list[str] = Field(description="Tracked documents whose Markdown file no longer exists.")
    semantic_index: RebuildReport = Field(description="Counters from rebuilding the semantic (tag) indexes.")
    sections_index: RebuildReport = Field(description="Counters from rebuilding the section indexes.")

    @property
    def complete(self) -> bool:
        """True when no model and no document had to be skipped."""
        return not (self.skipped_models or self.skipped_documents)
