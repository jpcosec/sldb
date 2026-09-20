"""A restriction to a subgraph region."""

from __future__ import annotations

from pydantic import BaseModel, Field


class GraphScope(BaseModel):
    """Restrict the query to a subgraph region."""

    descendant_of: str | None = Field(default=None, description="Only nodes reachable from this node.")
    ancestor_of: str | None = Field(default=None, description="Only nodes that reach this node.")
    node_id_prefix: str | None = Field(default=None, description="Only nodes whose id starts with this prefix.")
