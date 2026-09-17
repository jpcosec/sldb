"""One field of a registered model, as `describe_model` lists it."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ModelFieldSummary(BaseModel):
    """A model field's name, type and meaning."""

    name: str = Field(description="Field name as it appears in document payloads.")
    annotation: str = Field(description="Readable name of the field's declared type.")
    description: str = Field(description="The field's declared description; empty when it has none.")
