"""`transition_model`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TransitionModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    from_: str = Field(
        alias="from", description="Source state identifier for the transition."
    )
    to: str = Field(description="Destination state identifier for the transition.")
    on: str = Field(description="Event or trigger that causes the transition.")
    guard: str | None = Field(
        default=None,
        description="Optional guard condition that must be true for the transition.",
    )
    action: str | None = Field(
        default=None, description="Optional action executed during the transition."
    )
