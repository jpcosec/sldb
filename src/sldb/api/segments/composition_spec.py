"""The composition declaration behind a ``render`` field that assembles pieces."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class CompositionSpec(BaseModel):
    """How a composed field builds its text out of other documents or fields."""

    name: str = Field(description="Name of the composed field in the parent model.")
    source_field: str | None = Field(default=None, description="Field holding the references that are composed; None when the spec declares none.")
    model: str | None = Field(default=None, description="Class name of the model each reference is extracted with; None when unresolved.")
    ref: Literal["document", "field"] = Field(default="document", description="Whether each reference addresses a whole document or a single field.")
