"""Base común de los modelos de spec por tipo de diagrama."""

from sldb.models.notation.diagram_specs.base.base_diagram import BaseDiagram
from sldb.models.notation.diagram_specs.base.doc_ref import DOC_REF_PATTERN, DocRef
from sldb.models.notation.diagram_specs.base.extensions import EXTENSION_PREFIX, move_extensions
from sldb.models.notation.diagram_specs.base.metadata import Metadata
from sldb.models.notation.diagram_specs.base.style import Style
from sldb.notations.diagram_type import DiagramType

__all__ = ["BaseDiagram", "DOC_REF_PATTERN", "DocRef", "EXTENSION_PREFIX", "move_extensions", "Metadata", "Style", "DiagramType"]
