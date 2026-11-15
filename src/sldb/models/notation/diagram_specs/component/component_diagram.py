"""`component_diagram`."""

from __future__ import annotations

from typing import Literal
from pydantic import Field

from sldb.models.notation.diagram_specs.base.base_diagram import BaseDiagram
from sldb.models.notation.diagram_specs.component.component_data import ComponentData
from sldb.notations.diagram_type import DiagramType


class ComponentDiagram(BaseDiagram):
    type: Literal[DiagramType.component] = Field(
        default=DiagramType.component,
        description="Discriminator for component diagram specs.",
    )
    data: ComponentData = Field(
        description="Component-specific nodes and relationships."
    )
