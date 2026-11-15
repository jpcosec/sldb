"""`matrix_stage_model`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MatrixStageModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(description="Stable stage identifier used inside matrix views.")
    label: str = Field(description="Display label rendered for the stage column.")
