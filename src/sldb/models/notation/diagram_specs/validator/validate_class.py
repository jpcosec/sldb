"""`validate_class`."""

from __future__ import annotations

from sldb.models.notation.diagram_specs.class_diagram import ClassDiagram
from sldb.models.notation.diagram_specs.validator.check_inheritance_cycles import check_inheritance_cycles
from sldb.models.notation.diagram_specs.validator.check_members import check_members
from sldb.models.notation.diagram_specs.validator.check_relations import check_relations
from sldb.models.notation.diagram_specs.validator.validate_packages import validate_packages

def validate_class(d: ClassDiagram) -> None:
    check_members(d)
    parents = check_relations(d)
    check_inheritance_cycles(parents, d.id)
    validate_packages(d)
