"""What a rebuild of the edge index did, shard by shard."""

from __future__ import annotations

from pydantic import BaseModel, Field


class EdgeRebuildReport(BaseModel):
    """Counts of one `rebuild_edges_indexes` pass; a warm pass reports nothing written."""

    models_walked: int = Field(default=0, description="Models whose cache key had moved, so their documents were checked.")
    docs_written: int = Field(default=0, description="Documents whose shard was (re)built because it was missing or its hash_c, tags or rules moved.")
    docs_reused: int = Field(default=0, description="Documents compared and found current: shard left untouched.")
    docs_skipped_missing: int = Field(default=0, description="Tracked documents whose file is gone; they contribute nothing.")
    models_unresolved: list[str] = Field(default_factory=list, description="Models whose class could not be imported here: no field nodes, relation/anchor documents of theirs stay plain.")
