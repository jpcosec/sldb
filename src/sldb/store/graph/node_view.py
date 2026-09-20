"""The node an executor returns: the edge index's node plus its filtered edges."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from sldb.store.models import EdgeRecord


class GraphNode(BaseModel):
    """A node as query results see it: its record and the edges that passed the relation filters."""

    id: str = Field(description="Absolute node id.")
    node_type: str = Field(description="Node class: a model name, `sldb_model`, `semantic_tag`...")
    semantics: dict[str, Any] = Field(default_factory=dict, description="What the contributor knows about the node.")
    facets: dict[str, dict[str, Any]] = Field(default_factory=dict, description="Non-semantics facet payloads (`source`, `git`...).")
    edges: list[EdgeRecord] = Field(default_factory=list, description="The node's edges after relation filtering.")
