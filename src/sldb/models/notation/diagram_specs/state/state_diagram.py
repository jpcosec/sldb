"""`state_diagram`."""

from __future__ import annotations

from typing import Literal
from pydantic import Field

from sldb.models.notation.diagram_specs.base.base_diagram import BaseDiagram
from sldb.notations.diagram_type import DiagramType
from sldb.models.notation.diagram_specs.state.state_data import StateData


class StateDiagram(BaseDiagram):
    type: Literal[DiagramType.state] = Field(
        default=DiagramType.state, description="Discriminator for state diagram specs."
    )
    data: StateData = Field(
        description="State-specific lifecycle nodes and transitions."
    )
