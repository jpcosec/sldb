"""`check_relations`: las relaciones entre clases; devuelve los padres por herencia."""

from __future__ import annotations

from sldb.models.notation.diagram_specs.class_diagram import ClassDiagram
from sldb.notations.exceptions import ValidationError

def _check_multiplicity(multiplicity, d_id: str) -> None:
    if multiplicity and ".." in multiplicity:
        low, high = multiplicity.split("..")
        if high != "*" and int(low) > int(high):
            raise ValidationError(f"Inverted multiplicity '{multiplicity}' in {d_id}")


def _check_inheritance(relation, d_id: str) -> None:
    if relation.from_ == relation.to:
        raise ValidationError(f"Class cannot inherit from or realize itself in {d_id}")
    if relation.from_multiplicity or relation.to_multiplicity:
        raise ValidationError(f"Inheritance and realization do not have multiplicities in {d_id}")


def _check_relation(relation, d: ClassDiagram, parents: dict) -> None:
    classes = d.data.classes
    if relation.from_ not in classes or relation.to not in classes:
        raise ValidationError(f"Class relation references unknown class: {relation.from_} -> {relation.to} in {d.id}")
    if relation.relation in {"inheritance", "realization"}:
        _check_inheritance(relation, d.id)
        parents[relation.from_].append(relation.to)
    if relation.relation == "realization" and classes[relation.to].kind not in {"interface", "protocol"}:
        raise ValidationError(f"Realization target '{relation.to}' must be an interface or protocol in {d.id}")
    _check_multiplicity(relation.from_multiplicity, d.id)
    _check_multiplicity(relation.to_multiplicity, d.id)


def check_relations(d: ClassDiagram) -> dict[str, list[str]]:
    parents: dict[str, list[str]] = {ident: [] for ident in d.data.classes}
    for relation in d.data.relations:
        _check_relation(relation, d, parents)
    return parents
