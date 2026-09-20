"""One directed connection between nodes of the portable graph."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from sldb.store.graph.vocabulary import VocabularyTerm


class Edge(BaseModel):
    """A universal connection from a node to a target node."""

    target_id: str = Field(description="The ID of the target node this edge points to.")
    relation_type: VocabularyTerm = Field(description="The relation token this edge represents.")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional context for the edge.")
