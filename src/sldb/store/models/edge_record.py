"""One edge of the edge index, in the shape every reader gets back."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, SerializerFunctionWrapHandler, model_serializer


class EdgeRecord(BaseModel):
    """A typed, directed edge between two node ids."""

    source: str = Field(description="Node id the edge leaves from.")
    target: str = Field(description="Node id the edge points at.")
    relation: str = Field(description="Relation type token; names a tracked RelationTypeDoc.")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Edge context: `origin` (structural, schema, alias, relation_doc) and, for authored edges, relation_doc, condition, axis, reverse.")
    effects: dict[str, Any] | None = Field(default=None, description="What taking the edge does to the subject, `{sets, terminal}` with `{field}` filled; only `edges_holding` fills it, and it is left out of every dump while None.")

    @model_serializer(mode="wrap")
    def _without_absent_effects(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        """The dump, without `effects` when no reading filled it (every reading but edges_holding)."""
        dumped = handler(self)
        if self.effects is None:
            dumped.pop("effects", None)
        return dumped
