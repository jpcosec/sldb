"""An edge's effects on a subject: its `sets` with `{field}` filled from the subject, and `terminal`."""

from __future__ import annotations

import re
from typing import Any

import yaml

_FIELD = re.compile(r"\{([A-Za-z_]\w*)\}")


def effects_of(attributes: dict[str, Any] | None, subject: dict[str, Any]) -> dict[str, Any] | None:
    """`{"sets": ..., "terminal": ...}` of an edge whose `attributes` follow the transition convention.

    Absent or null `attributes`/`sets` are `sets = {}`; absent or null `terminal` is false; other
    keys stay out. `{field}` (where_subject's syntax) is filled only inside strings, each string
    of a list too, with the subject's scalar in its YAML form (true/false, numbers, strings as
    they are). None when a `{field}` is absent, null or not a scalar: the edge does not hold.
    """
    attributes = attributes or {}
    try:
        sets = {key: _resolved(value, subject) for key, value in (attributes.get("sets") or {}).items()}
    except LookupError:
        return None
    return {"sets": sets, "terminal": bool(attributes.get("terminal"))}


def _resolved(value: Any, subject: dict[str, Any]) -> Any:
    """`value` with `{field}` filled in its strings; LookupError when one cannot be."""
    if isinstance(value, list):
        return [_resolved(item, subject) for item in value]
    if not isinstance(value, str):
        return value
    return _FIELD.sub(lambda m: _written(subject.get(m.group(1)), m.group(1)), value)


def _written(value: Any, field: str) -> str:
    """The subject's scalar as text: a string as is, any other scalar in its YAML form."""
    if isinstance(value, str):
        return value
    if isinstance(value, (bool, int, float)):
        return yaml.safe_dump(value).split("\n", 1)[0]
    raise LookupError(field)
