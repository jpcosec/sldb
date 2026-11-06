"""The `LinkDoc` payload a notation sync writes."""

from __future__ import annotations

from typing import Any

from sldb.notations.notation import ANY_RELATION, notation_ref


def _head(notation: Any, link: Any) -> dict[str, Any]:
    """Identity and the relation the link draws."""
    return {
        "id": f"{notation.name}.{link.id}",
        "title": link.title or link.id,
        "notation": notation_ref(notation.name),
        "relation": link.relation,
        "relation_type": "" if link.relation == ANY_RELATION else f"RelationTypeDoc:reltype-{link.relation}",
        "model": link.model,
    }


def _drawing(link: Any) -> dict[str, Any]:
    """Line, ends and labels of the link."""
    return {
        "draw": link.draw,
        "line": link.line,
        "source_end": link.source_end,
        "target_end": link.target_end,
        "label": link.label,
        "source_label": link.source_label,
        "target_label": link.target_label,
    }


def link_payload(notation: Any, link: Any) -> dict[str, Any]:
    """The `LinkDoc` payload of one link of `notation`."""
    form = f"(model {link.model})" if link.model else f"(relation {link.relation})"
    return {
        **_head(notation, link),
        **_drawing(link),
        "ends": {k: e.model_dump() for k, e in link.ends.items()},
        "form": link.form or form,
        "description": link.description,
        "color": link.color or None,
    }
