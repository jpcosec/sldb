"""`BaseDiagram`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.base.metadata import Metadata
from sldb.models.notation.diagram_specs.base.style import Style
from sldb.notations.diagram_type import DiagramType

class BaseDiagram(BaseModel):
    """Base class for all diagram types. Subclasses must add a `data` field."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="Stable identifier for the diagram specification.")
    title: str = Field(description="Human-readable title shown in rendered output.")
    type: DiagramType = Field(
        description="Semantic diagram type used to select the schema and renderer flow."
    )
    version: str = Field(
        description="Schema or document version for the specification."
    )
    metadata: Metadata | None = Field(
        default=None,
        description="Optional authorship and descriptive metadata for the spec.",
    )
    style: Style | None = Field(
        default=None, description="Optional presentation hints for renderers."
    )
