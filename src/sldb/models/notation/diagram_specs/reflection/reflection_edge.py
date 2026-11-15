"""`reflection_edge`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.reflection.semantic_metadata import SemanticMetadata


class ReflectionEdge(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    from_: str = Field(alias="from", description="Source node identifier.")
    to: str = Field(description="Target node identifier.")
    relation: str = Field(
        default="relates", description="Semantic relationship type (e.g., depends_on, inherits)."
    )
    label: str | None = Field(
        default=None, description="Optional label shown alongside the relationship."
    )
    metadata: SemanticMetadata | None = Field(
        default=None, description="Optional 6D metadata for the edge."
    )
