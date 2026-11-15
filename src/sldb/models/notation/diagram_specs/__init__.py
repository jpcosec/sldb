"""Modelos de spec por tipo de diagrama, con su carga y su validación (migrados de spec2viz)."""

from sldb.models.notation.diagram_specs.activity import ActivityDiagram
from sldb.models.notation.diagram_specs.class_diagram import ClassDiagram
from sldb.models.notation.diagram_specs.component import ComponentDiagram
from sldb.models.notation.diagram_specs.deployment import DeploymentDiagram
from sldb.models.notation.diagram_specs.matrix import MatrixDiagram
from sldb.models.notation.diagram_specs.reflection import ReflectionDiagram
from sldb.models.notation.diagram_specs.sequence import SequenceDiagram
from sldb.models.notation.diagram_specs.state import StateDiagram

__all__ = ["ActivityDiagram", "ClassDiagram", "ComponentDiagram", "DeploymentDiagram", "MatrixDiagram", "ReflectionDiagram", "SequenceDiagram", "StateDiagram"]
