"""`sequence_diagram`."""

from __future__ import annotations

from typing import Literal
from pydantic import Field

from sldb.models.notation.diagram_specs.base.base_diagram import BaseDiagram
from sldb.notations.diagram_type import DiagramType
from sldb.models.notation.diagram_specs.sequence.sequence_data import SequenceData


class SequenceDiagram(BaseDiagram):
    type: Literal[DiagramType.sequence] = Field(
        default=DiagramType.sequence,
        description="Discriminator for sequence diagram specs.",
    )
    data: SequenceData = Field(
        description="Sequence-specific participants and messages."
    )
