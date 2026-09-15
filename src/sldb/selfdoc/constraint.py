"""Argument-group constraints retained during CLI extraction."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ExclusiveGroup(BaseModel):
    """A mutually exclusive group, including its required-selection rule."""

    required: bool = Field(description="Whether exactly one member must be supplied.")
    arguments: list[str] = Field(description="Destinations of the group's members.")
