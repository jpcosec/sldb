"""`matrix_diagram`."""

from __future__ import annotations

from typing import Literal
from pydantic import Field

from sldb.models.notation.diagram_specs.base.base_diagram import BaseDiagram
from sldb.notations.diagram_type import DiagramType
from sldb.models.notation.diagram_specs.matrix.matrix_data import MatrixData


class MatrixDiagram(BaseDiagram):
    type: Literal[DiagramType.component_view_matrix] = Field(
        default=DiagramType.component_view_matrix,
        description="Discriminator for component view matrix specs.",
    )
    data: MatrixData = Field(
        description="Matrix-specific views and component hierarchy."
    )
