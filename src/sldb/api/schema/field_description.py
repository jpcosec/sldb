"""A typed description of one model field, as returned by `describe_field`."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class FieldDescription(BaseModel):
    """What a form or a schema needs to know about one field of a model."""

    name: str = Field(description="Field name as it appears in document payloads.")
    kind: str = Field(description="Input kind: string, boolean, integer, number, object, enum, stringlist, enumlist, list or unknown.")
    required: bool = Field(description="Whether a payload must provide the field (it has no default).")
    enum: list[Any] | None = Field(default=None, description="Allowed values for enum kinds; None when the field is not an enumeration.")
    annotation: str = Field(description="Name of the declared annotation, Optional wrappers included.")
    description: str = Field(description="The field's declared description; empty when it has none.")
