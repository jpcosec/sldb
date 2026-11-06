"""The transition convention of `RelationDoc.attributes`: `sets` and `terminal`.

`sets` maps a field of the subject to the value the transition writes there: a YAML scalar
(null included) or a list of them. `terminal` is a boolean sldb only carries. Both may be
absent or null; any other key of `attributes` is free and outside the convention.
"""

from __future__ import annotations

import datetime
from typing import Any

SCALARS = (str, int, float, bool, datetime.date, type(None))


def check_transition_attributes(attributes: dict[str, Any]) -> dict[str, Any]:
    """`attributes` unchanged when `sets` and `terminal` follow the convention.

    Raises:
        ValueError: `terminal` is not a boolean, `sets` is not a map, or a value of `sets`
            is not a scalar or a list of scalars; the message names the key.
    """
    terminal = attributes.get("terminal")
    if terminal is not None and not isinstance(terminal, bool):
        raise ValueError(f"attributes.terminal must be a boolean, got {type(terminal).__name__} {terminal!r}")
    check_sets(attributes.get("sets"))
    return attributes


def check_sets(sets: Any) -> None:
    """Raise ValueError unless `sets` is absent (None) or a map of scalars or lists of scalars."""
    if sets is None:
        return
    if not isinstance(sets, dict):
        raise ValueError(f"attributes.sets must be a map of field to value, got {type(sets).__name__} {sets!r}")
    for key, value in sets.items():
        for item in value if isinstance(value, list) else [value]:
            if not isinstance(item, SCALARS):
                raise ValueError(f"attributes.sets.{key} must be a scalar or a list of scalars; it holds {_kind(item)} {item!r}")


def _kind(item: Any) -> str:
    """How a value that is not a scalar reads in an error."""
    return {dict: "a map", list: "a nested list"}.get(type(item), f"a {type(item).__name__}")
