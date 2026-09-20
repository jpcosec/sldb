"""A filter over a node's edges by relation type and direction."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class RelationFilter(BaseModel):
    """Filter edges by relation_type membership and direction."""

    relation_types: list[str] = Field(default_factory=list, description="Allow-list of relation types; empty = all types pass through.")
    direction: Literal["outgoing", "incoming", "both"] = Field(default="both", description="Which edges to consider relative to the source node.")
