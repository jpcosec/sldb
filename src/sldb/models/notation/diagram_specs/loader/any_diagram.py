"""`AnyDiagram`: la unión de los ocho tipos, discriminada por `type`, y su adaptador."""

from __future__ import annotations

from typing import Annotated, Union

from pydantic import Field, TypeAdapter

from sldb.models.notation.diagram_specs.activity import ActivityDiagram
from sldb.models.notation.diagram_specs.class_diagram import ClassDiagram
from sldb.models.notation.diagram_specs.component import ComponentDiagram
from sldb.models.notation.diagram_specs.deployment import DeploymentDiagram
from sldb.models.notation.diagram_specs.matrix import MatrixDiagram
from sldb.models.notation.diagram_specs.reflection import ReflectionDiagram
from sldb.models.notation.diagram_specs.sequence import SequenceDiagram
from sldb.models.notation.diagram_specs.state import StateDiagram
from sldb.notations.diagram_type import DiagramType

AnyDiagram = Annotated[
    Union[
        ClassDiagram,
        SequenceDiagram, StateDiagram, ComponentDiagram,
        ActivityDiagram, DeploymentDiagram, MatrixDiagram,
        ReflectionDiagram,
    ],
    Field(discriminator="type"),
]

ADAPTER: TypeAdapter[AnyDiagram] = TypeAdapter(AnyDiagram)
VALID_TYPES = {t.value for t in DiagramType}
