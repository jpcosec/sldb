"""Payload helpers: flatten, dotted lookup, `{field}` templates and `where` matching."""

from __future__ import annotations

import re
from typing import Any

_PLACEHOLDER = re.compile(r"\{([A-Za-z0-9_.]+)\}")


def flatten(payload: dict[str, Any]) -> dict[str, Any]:
    """The payload with keys from `data` copied to the top level; `data` does not overwrite."""
    data = payload.get("data") or {}
    out = dict(payload)
    for key, value in (data.items() if isinstance(data, dict) else []):
        out.setdefault(key, value)
    return out


def lookup(payload: dict[str, Any], path: str) -> Any:
    """`a.b.c` on nested dicts; None if any segment is missing."""
    value: Any = payload
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def _value(key: str, flat: dict[str, Any], payload: dict[str, Any]) -> str:
    """The text of one placeholder; containers and absent values are empty."""
    value = flat.get(key) if "." not in key else lookup(payload, key)
    return "" if value is None or isinstance(value, (dict, list)) else str(value)


def render_template(template: str, payload: dict[str, Any]) -> str:
    """`{field}` -> value from flattened payload (`{a.b}` with dot on raw payload); absent -> empty."""
    flat = flatten(payload)
    text = _PLACEHOLDER.sub(lambda match: _value(match.group(1), flat, payload), template)
    return re.sub(r"[ \t]{2,}", " ", text).strip()


def render_keyword(template: str, payload: dict[str, Any]) -> str:
    """Glyph stereotype (`«{kind}»`) interpolated as a label; if no text remains, omitted."""
    text = render_template(template or "", payload)
    return text if text.strip("«»<> \t") else ""


def matches(expression: str, payload: dict[str, Any]) -> bool:
    """Whether the `where` expression holds for the flattened payload; empty always holds."""
    if not expression:
        return True
    from sldb.api import where_matches

    return where_matches(expression, flatten(payload))
