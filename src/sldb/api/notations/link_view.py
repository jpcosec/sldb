"""The view of one link: which edge, which relation and how it is drawn."""

from __future__ import annotations

import re
from typing import Any

from sldb.api.notations.template_render import render_template
from sldb.notations.notation import ANY_RELATION
from sldb.notations.styling import resolve_line_color

_ORDER = re.compile(r"\.(\d+)-")


def link_order(relation_doc: str | None) -> int:
    """Position of the edge in the spec, extracted from `<spec>.<nn>-...`; 0 if absent."""
    match = _ORDER.search(relation_doc or "")
    return int(match.group(1)) if match else 0


def _relation(lp: dict[str, Any], rp: dict[str, Any]) -> str:
    """The relation drawn: the link's own, or the relation doc's for a wildcard link."""
    return lp["relation"] if lp["relation"] != ANY_RELATION else str(rp.get("relation_type") or "")


def _identity(source: str, target: str, link: dict, rp: dict[str, Any], doc: str | None, data: dict) -> dict[str, Any]:
    """Which edge it is: endpoints, relation, link, doc, order, condition and data."""
    relation = _relation(link["payload"], rp)
    return {
        "source": source, "target": target, "relation": relation, "link": link["ref"], "doc": doc,
        "order": link_order(doc), "condition": str(rp.get("condition") or ""), "data": data,
    }


def _presentation(lp: dict[str, Any], templated: dict[str, Any], palette: dict | None) -> dict[str, Any]:
    """How it is drawn: labels, line, ends and color."""
    return {
        "source_label": render_template(lp.get("source_label") or "", templated),
        "target_label": render_template(lp.get("target_label") or "", templated),
        "draw": lp.get("draw", "line"),
        "line": lp.get("line", "solid"),
        "source_end": lp.get("source_end", "none"),
        "target_end": lp.get("target_end", "open-arrow"),
        "label": render_template(lp.get("label") or "", templated),
        "color": resolve_line_color(lp, palette),
    }


def link_view(
    source: str,
    target: str,
    link: dict,
    relation_payload: dict[str, Any] | None,
    relation_doc: str | None,
    palette: dict | None = None,
) -> dict[str, Any]:
    """The resolved link between two nodes."""
    rp = relation_payload or {}
    attributes = dict(rp.get("attributes") or {})
    templated = {**rp, "data": attributes}
    identity = _identity(source, target, link, rp, relation_doc, attributes)
    return {**identity, **_presentation(link["payload"], templated, palette)}
