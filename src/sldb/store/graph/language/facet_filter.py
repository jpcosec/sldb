"""A filter over the conditions on one facet."""

from __future__ import annotations

from pydantic import BaseModel, Field

from sldb.store.graph.language.field_condition import FieldCondition


class FacetFilter(BaseModel):
    """Filter nodes by conditions on a specific facet's fields."""

    facet: str = Field(description="The facet name to filter on (`identity`, `semantics`, `source`...).")
    conditions: list[FieldCondition] = Field(default_factory=list, description="Conditions to satisfy together.")
