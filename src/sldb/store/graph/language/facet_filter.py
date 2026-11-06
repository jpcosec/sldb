"""A filter on one facet: a predicate of the language over that facet's fields."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class FacetFilter(BaseModel):
    """Filter nodes by a predicate (rules-language.md) on a specific facet's fields."""

    model_config = ConfigDict(extra="forbid")

    facet: str = Field(description="The facet name to filter on (`identity`, `semantics`, `source`...).")
    where: str = Field(default="", description="A predicate of the language over the facet's fields, without paths; empty is no condition.")
