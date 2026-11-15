"""`reflection_diagram`."""

from __future__ import annotations

from typing import Literal
from pydantic import Field

from sldb.models.notation.diagram_specs.base.base_diagram import BaseDiagram
from sldb.notations.diagram_type import DiagramType
from sldb.models.notation.diagram_specs.reflection.enforcement_artifact import EnforcementArtifact
from sldb.models.notation.diagram_specs.reflection.reflection_ir import ReflectionIR


class ReflectionDiagram(BaseDiagram):
    """Diagram type specifically for architectural reflection and enforcement."""

    type: Literal[DiagramType.reflection] = Field(
        default=DiagramType.reflection,
        description="Discriminator for reflection diagram specs.",
    )
    data: ReflectionIR = Field(
        description="The core semantic IR containing nodes and edges."
    )
    enforcement: EnforcementArtifact | None = Field(
        default=None,
        description="Optional condensed artifact for inward architectural enforcement.",
    )
