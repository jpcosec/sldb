"""A typed query over the knowledge graph."""

from __future__ import annotations

from pydantic import BaseModel, Field

from sldb.store.graph.language.facet_filter import FacetFilter
from sldb.store.graph.language.graph_scope import GraphScope
from sldb.store.graph.language.relation_filter import RelationFilter


class StructuredQuery(BaseModel):
    """A typed query: facet filters (intersection), a scope, and relation filters."""

    filters: list[FacetFilter] = Field(default_factory=list, description="Facet filters; a node must match them all.")
    relations: list[RelationFilter] = Field(default_factory=list, description="Edge filters; empty = no edge filtering.")
    scope: GraphScope | None = Field(default=None, description="Subgraph region to search.")
