"""Modelos de spec del tipo `class_diagram`."""

from sldb.models.notation.diagram_specs.class_diagram.aliases import Identifier
from sldb.models.notation.diagram_specs.class_diagram.aliases import MemberName
from sldb.models.notation.diagram_specs.class_diagram.aliases import TypeName
from sldb.models.notation.diagram_specs.class_diagram.aliases import Label
from sldb.models.notation.diagram_specs.class_diagram.aliases import Visibility
from sldb.models.notation.diagram_specs.class_diagram.aliases import Multiplicity
from sldb.models.notation.diagram_specs.class_diagram.class_parameter import ClassParameter
from sldb.models.notation.diagram_specs.class_diagram.class_attribute import ClassAttribute
from sldb.models.notation.diagram_specs.class_diagram.class_method import ClassMethod
from sldb.models.notation.diagram_specs.class_diagram.class_definition import ClassDefinition
from sldb.models.notation.diagram_specs.class_diagram.class_relation import ClassRelation
from sldb.models.notation.diagram_specs.class_diagram.class_package import ClassPackage
from sldb.models.notation.diagram_specs.class_diagram.class_data import ClassData
from sldb.models.notation.diagram_specs.class_diagram.class_diagram import ClassDiagram

__all__ = ["Identifier", "MemberName", "TypeName", "Label", "Visibility", "Multiplicity", "ClassParameter", "ClassAttribute", "ClassMethod", "ClassDefinition", "ClassRelation", "ClassPackage", "ClassData", "ClassDiagram"]
