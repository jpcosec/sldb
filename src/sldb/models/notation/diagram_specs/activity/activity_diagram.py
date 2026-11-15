"""`activity_diagram`."""

from __future__ import annotations

from typing import Literal
from pydantic import Field

from sldb.models.notation.diagram_specs.activity.activity_data import ActivityData
from sldb.models.notation.diagram_specs.base.base_diagram import BaseDiagram
from sldb.notations.diagram_type import DiagramType


class ActivityDiagram(BaseDiagram):
    type: Literal[DiagramType.activity] = Field(
        default=DiagramType.activity,
        description="Discriminator for activity diagram specs.",
    )
    data: ActivityData = Field(description="Activity-specific steps and control flow.")
