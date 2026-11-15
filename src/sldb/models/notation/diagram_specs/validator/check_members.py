"""`check_members`: atributos y métodos de cada clase."""

from __future__ import annotations

from sldb.models.notation.diagram_specs.class_diagram import ClassDiagram
from sldb.notations.exceptions import ValidationError

def _check_method(ident: str, method, signatures: set, d_id: str) -> None:
    parameters = [p.name for p in method.parameters]
    if len(parameters) != len(set(parameters)):
        raise ValidationError(f"Duplicate parameter in '{ident}.{method.name}' in {d_id}")
    signature = (method.name, tuple(p.type for p in method.parameters))
    if signature in signatures:
        raise ValidationError(f"Duplicate method signature in '{ident}.{method.name}' in {d_id}")
    signatures.add(signature)
    if method.static and method.abstract:
        raise ValidationError(f"Method '{ident}.{method.name}' cannot be both static and abstract in {d_id}")


def check_members(d: ClassDiagram) -> None:
    for ident, definition in d.data.classes.items():
        names = [a.name for a in definition.attributes]
        if len(names) != len(set(names)):
            raise ValidationError(f"Duplicate attribute in class '{ident}' in {d.id}")
        signatures: set = set()
        for method in definition.methods:
            _check_method(ident, method, signatures, d.id)
