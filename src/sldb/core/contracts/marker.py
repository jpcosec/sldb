from typing import Any
from pydantic import BaseModel, Field

def parse_marker(inner: str) -> "Marker":
    head, _, prop = inner.partition("•")
    parts = _split_marker_head(head)
    kind = parts[0] if parts else "rev"
    traits = parts[1:] if parts else []
    name = prop.strip() if prop else ""
    return Marker(kind=kind, traits=traits, name=name)

def _split_marker_head(head: str) -> list[str]:
    parts, current, bracket_depth = [], [], 0
    for char in head:
        bracket_depth = _update_bracket_depth(char, bracket_depth)
        if char == "," and bracket_depth == 0:
            _append_part_and_reset(parts, current)
            continue
        current.append(char)
    _append_part_and_reset(parts, current)
    return parts

def _update_bracket_depth(char: str, bracket_depth: int) -> int:
    if char == "[":
        return bracket_depth + 1
    if char == "]" and bracket_depth:
        return bracket_depth - 1
    return bracket_depth

def _append_part_and_reset(parts: list[str], current: list[str]) -> None:
    part = "".join(current).strip()
    if part:
        parts.append(part)
    current.clear()

class Marker(BaseModel):
    """First-class representation of an SLDB marker."""
    kind: str = Field(description="The marker kind (e.g., 'rev', 'optrev', 'render', 'py').")
    traits: list[str] = Field(default_factory=list, description="Optional traits/modifiers for the marker.")
    name: str = Field(description="The name of the property or expression the marker refers to.")

    @property
    def is_reversible(self) -> bool:
        return self.kind == "rev"

    @property
    def is_optional(self) -> bool:
        return self.kind == "optrev"


def recipe_is_optional(recipe: dict[str, Any]) -> bool:
    """Whether the recipe's single field may be absent from the payload.

    Lives beside `Marker` because it answers a question about the marker, not
    about extraction: both capture paths ask it, and neither owns it.
    """
    props_info = recipe.get("props_info") or []
    return bool(props_info) and props_info[0].is_optional
