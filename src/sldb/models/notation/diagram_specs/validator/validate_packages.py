"""`validate_packages`: paquetes UML de un diagrama de clases."""

from __future__ import annotations

from sldb.models.notation.diagram_specs.class_diagram import ClassDiagram
from sldb.models.notation.diagram_specs.validator.containment import check_containment_cycles
from sldb.notations.exceptions import StructureError, UnknownReferenceError

def _add_member(parent: dict, d: ClassDiagram, pid: str, ref: str) -> None:
    if ref not in d.data.classes and ref not in d.data.packages:
        raise UnknownReferenceError(f"Package '{pid}' contains unknown class or package '{ref}' in {d.id}")
    if ref == pid:
        raise StructureError(f"Package '{pid}' contains itself in {d.id}")
    if ref in parent:
        what = "Class" if ref in d.data.classes else "Package"
        raise StructureError(f"{what} '{ref}' is contained by both '{parent[ref]}' and '{pid}' in {d.id}")
    parent[ref] = pid


def _package_parents(d: ClassDiagram) -> dict[str, str]:
    parent: dict[str, str] = {}
    for pid, package in d.data.packages.items():
        for ref in package.contains:
            _add_member(parent, d, pid, ref)
    return parent


def validate_packages(d: ClassDiagram) -> None:
    """Paquetes UML: ids unicos frente a las clases, contenidos que existen, un padre por clase y
    por paquete, sin ciclos, y (si hay paquetes) ninguna clase huerfana."""
    classes, packages = d.data.classes, d.data.packages
    if not packages:
        return
    for both in sorted(set(classes) & set(packages)):
        raise StructureError(f"Id '{both}' is both a class and a package in {d.id}")
    parent = _package_parents(d)
    check_containment_cycles(parent, packages, "Package", d.id)
    orphans = sorted(c for c in classes if c not in parent)
    if orphans:
        raise StructureError(f"Orphan class(es) {', '.join(orphans)}: the spec declares packages, so every class belongs to one, in {d.id}")
