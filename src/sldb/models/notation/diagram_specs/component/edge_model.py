"""`edge_model`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class EdgeModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    from_: str = Field(alias="from", description="Source component identifier.")
    to: str = Field(description="Destination component identifier.")
    relation: str = Field(
        default="uses",
        description="Semantic relationship between the connected components.",
    )
    label: str | None = Field(
        default=None, description="Optional label shown alongside the relationship."
    )
