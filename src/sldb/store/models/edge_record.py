"""One edge of the edge index, in the shape every reader gets back."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class EdgeRecord(BaseModel):
    """A typed, directed edge between two node ids."""

    source: str = Field(description="Node id the edge leaves from.")
    target: str = Field(description="Node id the edge points at.")
    relation: str = Field(description="Relation type token; names a tracked RelationTypeDoc.")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Edge context: `origin` (structural, schema, alias, relation_doc) and, for authored edges, relation_doc, condition, axis, reverse.")
