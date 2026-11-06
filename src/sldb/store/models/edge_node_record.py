"""One node of the edge index: its id, its class, and what the index knows about it."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, model_serializer

#: The document-only fields: left out of a dump while empty, so other nodes' shards do not grow.
PROJECTION_FIELDS = ("payload", "field_hashes", "source_hash", "contract_signature")


class EdgeNodeRecord(BaseModel):
    """A node a shard contributes to the edge index (document, section, model, field, tag...)."""

    id: str = Field(description="Absolute node id, `sldb://<kind>/<name>`; the key edges point at.")
    node_type: str = Field(description="Node class the relation types validate against: a model name for a document, else `sldb_model`, `sldb_field`, `semantic_tag`...")
    semantics: dict[str, Any] = Field(default_factory=dict, description="What the contributor knows about the node (a document's path and tags, a field's type, a relation type's payload).")
    facets: dict[str, dict[str, Any]] = Field(default_factory=dict, description="Non-semantics facet payloads (`source` provenance, `git`...); filled on read, not persisted in the shards.")
    payload: dict[str, Any] = Field(default_factory=dict, description="A document's projected payload: its top-level fields holding a scalar or a list of scalars (or exactly the model's `__indexed__`); nested values are left out. Empty on any other node.")
    field_hashes: dict[str, str] = Field(default_factory=dict, description="A document's whole field_hashes map, as its index entry records it. Empty on any other node.")
    source_hash: str = Field(default="", description="A document's source_hash (hash_c) the node was built from. Empty on any other node.")
    contract_signature: str = Field(default="", description="sha256 of the model's fields, __references__, __containment__ and __compositions__ names the node was built under; empty when the model could not be loaded, or on any other node.")

    @model_serializer(mode="wrap")
    def _drop_empty_projection(self, handler: Any) -> Any:
        data = handler(self)
        if isinstance(data, dict):
            for key in PROJECTION_FIELDS:
                if not data.get(key):
                    data.pop(key, None)
        return data
