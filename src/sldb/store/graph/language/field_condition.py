"""One comparison condition on a facet field."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class FieldCondition(BaseModel):
    """A single comparison condition on a facet field."""

    field: str = Field(description="Name of the field within the facet.")
    op: Literal["eq", "ne", "is_null", "is_not_null", "contains", "gt", "lt", "starts_with"] = Field(description="The comparison operator.")
    value: Any = Field(default=None, description="The value to compare against; ignored by the null operators.")
