"""The parts of a `ViewDoc` section (GD25): an edges entry, and the normalizers of its other keys."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_serializer

DIRECTIONS = ("out", "in")
TRANSITION_KEYS = ("from_field", "relation")


class ViewEdge(BaseModel):
    """The neighbours of each row along one relation, in one direction, under one row key."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    relation: str = Field(description="Relation type of the edges followed.")
    direction: str = Field(description="`out` (edges leaving the row) or `in` (edges reaching it).")
    key: str = Field(default="", alias="as", description="Row key the neighbour ids go under; `<direction>:<relation>` when absent.")

    @field_validator("relation")
    @classmethod
    def _named(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("an edges entry needs a relation")
        return value

    @field_validator("direction")
    @classmethod
    def _direction(cls, value: str) -> str:
        if value not in DIRECTIONS:
            raise ValueError(f"direction {value!r} must be out or in")
        return value

    @model_serializer(mode="wrap")
    def _as_declared(self, handler) -> dict[str, Any]:
        """The dump names the key `as`, as the document declares it."""
        dumped = handler(self)
        return {"relation": dumped["relation"], "direction": dumped["direction"], "as": dumped["key"]}

    def row_key(self) -> str:
        """`as`, else `<direction>:<relation>`."""
        return self.key or f"{self.direction}:{self.relation}"


def normalize_transitions(value: Any) -> dict[str, str] | None:
    """`{from_field, relation}` with both non-blank, or None when absent."""
    if value is None:
        return None
    if not isinstance(value, dict) or set(value) != set(TRANSITION_KEYS):
        raise ValueError(f"transitions must be a mapping with exactly {list(TRANSITION_KEYS)}, got {value!r}")
    cleaned = {key: str(value[key] or "").strip() for key in TRANSITION_KEYS}
    if not all(cleaned.values()):
        raise ValueError("transitions.from_field and transitions.relation cannot be blank")
    return cleaned


def normalize_names(value: Any, what: str) -> list[str]:
    """A list of non-blank strings; None is the empty list."""
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"{what} must be a list of non-blank strings, got {value!r}")
    return list(value)
