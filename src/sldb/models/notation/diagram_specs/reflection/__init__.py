"""Modelos de spec del tipo `reflection`."""

from sldb.models.notation.diagram_specs.reflection.semantic_metadata import SemanticMetadata
from sldb.models.notation.diagram_specs.reflection.reflection_node import ReflectionNode
from sldb.models.notation.diagram_specs.reflection.reflection_edge import ReflectionEdge
from sldb.models.notation.diagram_specs.reflection.reflection_ir import ReflectionIR
from sldb.models.notation.diagram_specs.reflection.enforcement_fact import EnforcementFact
from sldb.models.notation.diagram_specs.reflection.enforcement_artifact import EnforcementArtifact
from sldb.models.notation.diagram_specs.reflection.reflection_diagram import ReflectionDiagram

__all__ = ["SemanticMetadata", "ReflectionNode", "ReflectionEdge", "ReflectionIR", "EnforcementFact", "EnforcementArtifact", "ReflectionDiagram"]
