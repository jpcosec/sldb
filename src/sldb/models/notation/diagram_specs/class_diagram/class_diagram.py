"""`class_diagram`."""

from __future__ import annotations

from typing import Literal
from pydantic import ConfigDict

from sldb.models.notation.diagram_specs.base.base_diagram import BaseDiagram
from sldb.models.notation.diagram_specs.class_diagram.class_data import ClassData
from sldb.notations.diagram_type import DiagramType


class ClassDiagram(BaseDiagram):
    model_config = ConfigDict(extra="forbid")
    type: Literal[DiagramType.class_] = DiagramType.class_
    data: ClassData
