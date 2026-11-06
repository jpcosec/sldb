"""Coherencia interna de una notacion: ids, glifos por defecto y relaciones."""

from __future__ import annotations

from typing import Any

from sldb.notations.notation_constants import ANY_RELATION, KNOWN_RELATIONS


def _duplicate_ids(spec: Any) -> list[str]:
    problems: list[str] = []
    for what, items in (("glyph", spec.glyphs), ("link", spec.links), ("marker", spec.markers)):
        ids = [i.id for i in items]
        for dup in sorted({i for i in ids if ids.count(i) > 1}):
            problems.append(f"{what} id {dup!r} is declared more than once")
    return problems


def _missing_defaults(spec: Any) -> list[str]:
    models = {g.model for g in spec.glyphs}
    return [
        f"model {model!r} has no default glyph (one without `where`)"
        for model in sorted(models)
        if not any(g.model == model and not g.where for g in spec.glyphs)
    ]


def _unknown_relations(spec: Any) -> list[str]:
    known = KNOWN_RELATIONS.get(spec.diagram_type)
    if known is None:
        return []
    return [
        f"link {link.id!r} draws relation {link.relation!r}, which a `{spec.diagram_type}` spec never emits "
        f"(known: {', '.join(sorted(known))})"
        for link in spec.links
        if link.relation != ANY_RELATION and link.relation not in known
    ]


def _repeated_relations(spec: Any) -> list[str]:
    relations = [l.relation for l in spec.links if not l.model]
    return [f"relation {dup!r} is drawn by more than one link" for dup in sorted({r for r in relations if relations.count(r) > 1})]


def notation_problems(spec: Any) -> list[str]:
    """Los problemas de coherencia de una notacion, en el orden en que se reportan."""
    return [*_duplicate_ids(spec), *_missing_defaults(spec), *_unknown_relations(spec), *_repeated_relations(spec)]
