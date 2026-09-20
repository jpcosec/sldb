"""The formal envelope for query results."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from sldb.store.graph.node import KnowledgeNode


class QueryResult(BaseModel):
    """Primary matches plus optionally their structural neighborhood."""

    primary_ids: list[str] = Field(description="IDs of nodes that explicitly matched the query filters.")
    nodes: list[KnowledgeNode] = Field(description="The set of nodes comprising both primary matches and their neighborhood.")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Execution metadata.")
