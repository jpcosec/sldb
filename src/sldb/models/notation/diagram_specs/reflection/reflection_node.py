"""`reflection_node`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.reflection.semantic_metadata import SemanticMetadata


class ReflectionNode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: str = Field(
        default="core", description="Semantic kind of the node (e.g., repository, module)."
    )
    label: str | None = Field(
        default=None, description="Optional display label for the node."
    )
    metadata: SemanticMetadata | None = Field(
        default=None, description="Optional 6D metadata for the node."
    )
