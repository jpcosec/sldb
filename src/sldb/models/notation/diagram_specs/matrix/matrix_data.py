"""`matrix_data`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.matrix.matrix_component_model import MatrixComponentModel
from sldb.models.notation.diagram_specs.matrix.matrix_view_model import MatrixViewModel


class MatrixData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    views: list[MatrixViewModel] = Field(
        description="Matrix views that define the column layout."
    )
    components: list[MatrixComponentModel] = Field(
        description="Top-level components rendered as rows in the matrix."
    )
