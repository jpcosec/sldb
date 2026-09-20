"""One node of the edge index: its id, its class, and what the index knows about it."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class EdgeNodeRecord(BaseModel):
    """A node a shard contributes to the edge index (document, section, model, field, tag...)."""

    id: str = Field(description="Absolute node id, `sldb://<kind>/<name>`; the key edges point at.")
    node_type: str = Field(description="Node class the relation types validate against: a model name for a document, else `sldb_model`, `sldb_field`, `semantic_tag`...")
    semantics: dict[str, Any] = Field(default_factory=dict, description="What the contributor knows about the node (a document's path and tags, a field's type, a relation type's payload).")
    facets: dict[str, dict[str, Any]] = Field(default_factory=dict, description="Non-semantics facet payloads (`source` provenance, `git`...); filled on read, not persisted in the shards.")
