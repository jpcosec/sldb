"""`validate`: la validación semántica de un spec cargado."""

from __future__ import annotations

from sldb.models.notation.diagram_specs.base.base_diagram import BaseDiagram
from sldb.models.notation.diagram_specs.class_diagram import ClassDiagram
from sldb.models.notation.diagram_specs.component import ComponentDiagram
from sldb.models.notation.diagram_specs.activity import ActivityDiagram
from sldb.models.notation.diagram_specs.deployment import DeploymentDiagram
from sldb.models.notation.diagram_specs.matrix import MatrixDiagram
from sldb.models.notation.diagram_specs.sequence import SequenceDiagram
from sldb.models.notation.diagram_specs.state import StateDiagram
from sldb.models.notation.diagram_specs.validator.validate_activity import validate_activity
from sldb.models.notation.diagram_specs.validator.validate_class import validate_class
from sldb.models.notation.diagram_specs.validator.validate_component import validate_component
from sldb.models.notation.diagram_specs.validator.validate_deployment import validate_deployment
from sldb.models.notation.diagram_specs.validator.validate_matrix import validate_matrix
from sldb.models.notation.diagram_specs.validator.validate_sequence import validate_sequence
from sldb.models.notation.diagram_specs.validator.validate_state import validate_state
from sldb.models.notation.diagram_specs.validator.validate_style import validate_style

def validate(diagram: BaseDiagram) -> None:
    validate_style(diagram)
    match diagram:
        case ClassDiagram():      validate_class(diagram)
        case ComponentDiagram():  validate_component(diagram)
        case SequenceDiagram():   validate_sequence(diagram)
        case StateDiagram():      validate_state(diagram)
        case ActivityDiagram():   validate_activity(diagram)
        case DeploymentDiagram(): validate_deployment(diagram)
        case MatrixDiagram():     validate_matrix(diagram)
