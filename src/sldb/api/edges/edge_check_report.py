"""Outcome of checking a store's edge index, as returned by `check_edges`."""

from __future__ import annotations

from pydantic import BaseModel, Field


class EdgeCheckReport(BaseModel):
    """The edge index's validation errors, reported instead of raised: the index is still readable."""

    errors: list[str] = Field(default_factory=list, description="Authored edges to documents that are not tracked, edges of unknown relation types, endpoint classes a type does not allow, cardinality violations.")
    stale: list[str] = Field(default_factory=list, description="Export ids of documents whose shard is not built from their current hash_c.")
    untracked_builtins: list[str] = Field(default_factory=list, description="Builtin relation types sldb's derived edges use that the store does not track; validated against the shipped definition, not an error. `sldb edges init` tracks them.")

    linked_errors: list[str] = Field(default_factory=list, description="Violations committed only by edges a linked store contributes: that store's to fix, reported here without failing this check.")
    linked_stale: list[str] = Field(default_factory=list, description="Stale documents of linked stores (`store:Model:name`): rebuild there.")

    @property
    def ok(self) -> bool:
        """True when this store's part of the index is current and every one of its edges is valid."""
        return not (self.errors or self.stale)
