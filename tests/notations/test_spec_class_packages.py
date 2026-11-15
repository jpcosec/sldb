from pathlib import Path

import pytest

from sldb.models.notation.diagram_specs.class_diagram import ClassPackage
from sldb.models.notation.diagram_specs.loader import load
from sldb.models.notation.diagram_specs.validator import validate
from sldb.notations.exceptions import StructureError, UnknownReferenceError

SPEC = Path(__file__).parent.parent / "fixtures" / "specs" / "class.packages.yml"


@pytest.mark.parametrize("mutate, error, message", [
    (lambda d: d.data.packages["shared"].contains.append("Ghost"), UnknownReferenceError, "unknown class or package 'Ghost'"),
    (lambda d: d.data.packages["shared"].contains.append("shared"), StructureError, "contains itself"),
    (lambda d: d.data.packages["shared"].contains.append("Invoice"), StructureError, "Class 'Invoice' is contained by both"),
    (lambda d: d.data.packages["shared"].contains.append("billing"), StructureError, "Package 'billing' is contained by both"),
    (lambda d: d.data.packages["billing"].contains.append("core"), StructureError, "cycle"),
    (lambda d: d.data.packages["shared"].contains.remove("AuditLog"), StructureError, "Orphan class"),
])
def test_typed_validation(mutate, error, message):
    diagram = load(SPEC)
    mutate(diagram)
    with pytest.raises(error, match=message):
        validate(diagram)


def test_package_id_cannot_be_a_class_id():
    diagram = load(SPEC)
    diagram.data.packages["User"] = ClassPackage(contains=[])
    with pytest.raises(StructureError, match="both a class and a package"):
        validate(diagram)
