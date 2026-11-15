"""`matrix_component_model`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MatrixComponentModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(
        description="Stable component identifier used within the matrix hierarchy."
    )
    kind: str = Field(
        default="core", description="Semantic category assigned to the component."
    )
    label: str | None = Field(
        default=None, description="Optional display name for the component."
    )
    stages: dict[str, list[str]] = Field(
        default_factory=dict,
        description="View-to-stage membership mapping for the component.",
    )
    children: list[MatrixComponentModel] = Field(
        default_factory=list,
        description="Nested child components rendered beneath this component.",
    )


MatrixComponentModel.model_rebuild()
