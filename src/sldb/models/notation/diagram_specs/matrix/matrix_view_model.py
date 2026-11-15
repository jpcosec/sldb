"""`matrix_view_model`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.matrix.matrix_stage_model import MatrixStageModel


class MatrixViewModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(description="Stable identifier for the matrix view.")
    label: str = Field(description="Display label rendered for the view.")
    stages: list[MatrixStageModel] = Field(
        description="Ordered stages shown within the view."
    )
