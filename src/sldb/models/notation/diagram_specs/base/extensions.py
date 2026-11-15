"""Anotaciones del proyecto (`x-*`) de un spec."""

from __future__ import annotations

from typing import Any

#: Prefix of the project annotations a spec may add under ``metadata`` and activity steps (OpenAPI-style ``x-`` extensions).
EXTENSION_PREFIX = "x-"


def move_extensions(value: Any) -> Any:
    """Move every ``x-*`` key of a raw mapping into its ``extensions`` entry (a ``mode="before"`` helper)."""
    if not isinstance(value, dict):
        return value
    value = dict(value)
    found = {k: value.pop(k) for k in list(value) if isinstance(k, str) and k.startswith(EXTENSION_PREFIX)}
    if found:
        value["extensions"] = {**(value.get("extensions") or {}), **found}
    return value
