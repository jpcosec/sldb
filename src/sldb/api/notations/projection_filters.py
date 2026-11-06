"""What a projection view selects: node entries, relation filter and titles."""

from __future__ import annotations

from typing import Any

from sldb.api.notations.projection_constants import DIRECTIONS
from sldb.api.notations.template_render import flatten
from sldb.api.notations.view_error import ViewError


def view_entries(view: dict[str, Any]) -> list[dict[str, str]]:
    """The `{model, where}` entries of the view; ViewError if malformed."""
    entries = view.get("nodes") or []
    if not isinstance(entries, list) or not all(isinstance(e, dict) and e.get("model") for e in entries):
        raise ViewError("nodes must be a list of {model, where}")
    return [{"model": str(e["model"]), "where": str(e.get("where") or "")} for e in entries]


def relation_filter(view: dict[str, Any]) -> tuple[list[str], str]:
    """The `(relations, direction)` of the view; ViewError if malformed."""
    relations = view.get("relations") or []
    direction = view.get("direction") or "both"
    if not isinstance(relations, list) or direction not in DIRECTIONS:
        raise ViewError(f"relations must be a list and direction one of {', '.join(DIRECTIONS)}")
    return [str(r) for r in relations], direction


def plan(view: dict[str, Any]) -> tuple[list[dict[str, str]], list[str], str]:
    """The validated `(entries, relations, direction)` of the view."""
    entries = view_entries(view)
    relations, direction = relation_filter(view)
    return entries, relations, direction


def is_selected(doc: Any, entries: list[dict[str, str]]) -> bool:
    """Whether `doc` matches some entry; no entries select everything."""
    if not entries:
        return True
    from sldb.api.where import where_matches

    try:
        flat = flatten(doc.payload or {})
        return any(e["model"] == doc.model_name and where_matches(e["where"], flat) for e in entries)
    except Exception as exc:
        raise ViewError(f"where does not parse: {exc}") from exc


def doc_title(doc: Any) -> str:
    """The title, name or doc name, in that order."""
    payload = doc.payload or {}
    return str(payload.get("title") or payload.get("name") or doc.name)
