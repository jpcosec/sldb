"""A registered model that could not be described, and why.

Degrading a schema listing means the consumer must be told what is missing.
Omitting the broken model silently would leave a UI drawing a store with fewer
models than it has and no way to know that: an unavailable model is reported,
not skipped.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class UnavailableModel(BaseModel):
    """A model registered in the store whose class could not be loaded."""

    model: str = Field(description="Name of the registered model that failed to load.")
    model_ref: str = Field(description="The registered ``module:Class`` reference that could not be resolved.")
    error: str = Field(description="Why the model is unavailable, as a human-readable message.")
