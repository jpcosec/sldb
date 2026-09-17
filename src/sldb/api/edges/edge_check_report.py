"""Outcome of checking a store's edge index, as returned by `check_edges`."""

from __future__ import annotations

from pydantic import BaseModel, Field


class EdgeCheckReport(BaseModel):
    """What kgdb raised as TypedIngestError, reported instead: the index is still readable."""

    errors: list[str] = Field(default_factory=list, description="Authored edges to documents that are not tracked, edges of unknown relation types, endpoint classes a type does not allow, cardinality violations.")
    stale: list[str] = Field(default_factory=list, description="Export ids of documents whose shard is not built from their current hash_c.")

    @property
    def ok(self) -> bool:
        """True when the index is current and every edge is valid."""
        return not (self.errors or self.stale)
