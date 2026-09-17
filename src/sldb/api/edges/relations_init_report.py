"""Outcome of preparing a store for typed relations, as returned by `init_relations`."""

from __future__ import annotations

from pydantic import BaseModel, Field


class RelationsInitReport(BaseModel):
    """What `init_relations` had to do; all empty on a store that was already prepared."""

    models_added: list[str] = Field(default_factory=list, description="Model references registered by this call (RelationTypeDoc, RelationDoc).")
    models_repointed: list[str] = Field(default_factory=list, description="Models that were registered from `kgdb.models` and now import from sldb.")
    types_written: list[str] = Field(default_factory=list, description="Builtin relation types written and tracked as RelationTypeDoc documents.")
    predicates_added: list[str] = Field(default_factory=list, description="Relation names registered as sldb predicates with their axis.")

    def summary(self) -> str:
        """One line for a CLI or a log."""
        return f"models added: {len(self.models_added)} · builtin relation types written: {len(self.types_written)} · predicates added: {len(self.predicates_added)}"
