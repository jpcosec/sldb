"""A `--where` field by dotted path, so a nested value and the `sldb` provenance block are addressable."""

from __future__ import annotations

from typing import Any

_ABSENT = object()


def _lookup(payload: Any, field: str, default: Any = None) -> Any:
    """A field by dotted path (`sldb.authority`, `tasks.0.title`), `default` when absent."""
    value = payload
    for part in field.split("."):
        if isinstance(value, dict) and part in value:
            value = value[part]
        elif isinstance(value, list) and part.isdigit() and int(part) < len(value):
            value = value[int(part)]
        else:
            return default
    return value
