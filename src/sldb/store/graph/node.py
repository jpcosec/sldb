"""A knowledge node of the portable graph: identity, edges and facet slots."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from sldb.store.graph.edge import Edge
from sldb.store.graph.facet import FacetPayload
from sldb.store.graph.identity import SystemIdentity


class KnowledgeNode(BaseModel):
    """Any element of the system, from a store to a section to a function."""

    model_config = ConfigDict(validate_assignment=True)

    identity: SystemIdentity = Field(description="The unique identity and type of this node.")
    edges: list[Edge] = Field(default_factory=list, description="Directed connections to other nodes.")
    semantics: FacetPayload | None = Field(default=None, description="Semantic information like intent and raw docstrings.")
    ast: FacetPayload | None = Field(default=None, description="AST information about code structure.")
    io_ports: list[FacetPayload] = Field(default_factory=list, description="Details about input/output ports.")
    compliance: FacetPayload | None = Field(default=None, description="Compliance status against defined standards.")
    adr: FacetPayload | None = Field(default=None, description="Architectural Decision Record information.")
    test_map: FacetPayload | None = Field(default=None, description="Testing strategy and coverage.")
    git: FacetPayload | None = Field(default=None, description="Git metadata for file-backed or doc-backed nodes.")
    source: FacetPayload | None = Field(default=None, description="Provenance and source tracking metadata.")

    @field_validator("semantics", "ast", "compliance", "adr", "test_map", "git", "source", mode="before")
    @classmethod
    def _coerce_facet(cls, value: object) -> object:
        if isinstance(value, BaseModel):
            return value.model_dump()
        return value

    @field_validator("io_ports", mode="before")
    @classmethod
    def _coerce_facet_list(cls, value: object) -> object:
        if not isinstance(value, list):
            return value
        return [item.model_dump() if isinstance(item, BaseModel) else item for item in value]
