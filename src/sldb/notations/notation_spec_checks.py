"""The shape checks `NotationSpec` runs over its `standard` and `layout` fields."""

from __future__ import annotations

from typing import Any

from sldb.notations.notation_constants import LAYOUT_KINDS


def _check_standard_shape(who: Any, std: Any) -> None:
    """Raise, naming the notation, unless `std` is a mapping with a name and an optional version."""
    if not isinstance(std, dict):
        raise ValueError(f"notation {who!r}: standard must be a mapping with name and optional version")
    if not isinstance(std.get("name"), str) or not std["name"].strip():
        raise ValueError(f"notation {who!r}: standard.name is required and must be non-empty (version alone is not a standard)")
    if "version" in std and std["version"] is not None and (not isinstance(std["version"], str) or not std["version"].strip()):
        raise ValueError(f"notation {who!r}: standard.version must be a non-empty string when present")


def _check_layout(kind: str, v: dict) -> None:
    """Raise unless the layout's kind, direction and style are recognised."""
    if kind not in LAYOUT_KINDS:
        raise ValueError(f"layout.kind {kind!r} is not one of {', '.join(LAYOUT_KINDS)}")
    if "direction" in v and v["direction"] not in ("TB", "LR", "BT", "RL"):
        raise ValueError(f"layout.direction {v['direction']!r} must be TB, LR, BT or RL")
    # parametros reconocidos de kind graph: style layered|rings, ring_field para rings
    if v.get("style") not in (None, "layered", "rings"):
        raise ValueError(f"layout.style {v['style']!r} must be layered or rings")


def _layout_by(kind: str, by: Any) -> str:
    """`layout.by` stripped; it only applies to partition-lanes and must name a field."""
    if kind != "partition-lanes":
        raise ValueError("layout.by only applies to kind partition-lanes")
    if not isinstance(by, str) or not by.strip():
        raise ValueError("layout.by must be a non-empty field name")
    return by.strip()



