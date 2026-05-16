from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, Field


MARKER_PATTERN = r"⸢([^⸥]+)⸥"
"""Canonical regex matching the full marker syntax ⸢...⸥ and capturing inner content."""


def parse_marker(inner: str) -> "Marker":
    """
    Parses the inner content of a marker into components.

    Args:
        inner: The content inside ⸢...⸥ (e.g. ``"rev,list•name"``).

    Returns:
        A Marker model instance.
    """
    head, _, prop = inner.partition("•")
    parts = [part.strip() for part in head.split(",") if part.strip()]
    kind = parts[0] if parts else "rev"
    traits = parts[1:] if parts else []
    name = prop.strip() if prop else ""
    return Marker(kind=kind, traits=traits, name=name)


class Marker(BaseModel):
    """
    First-class representation of an SLDB marker ⸢kind,trait•name⸥.
    """

    kind: str = Field(
        description="The marker kind (e.g., 'rev', 'optrev', 'render', 'py')."
    )
    traits: list[str] = Field(
        default_factory=list, description="Optional traits/modifiers for the marker."
    )
    name: str = Field(
        description="The name of the property or expression the marker refers to."
    )

    @property
    def is_reversible(self) -> bool:
        """Returns True if the marker is a reversible source of truth."""
        return self.kind == "rev"

    @property
    def is_optional(self) -> bool:
        """Returns True if the marker is an optional mirror."""
        return self.kind == "optrev"


class NodeData(BaseModel):
    """
    Contract for data extracted from a Markdown node.

    This ensures that node handlers return structured data instead of raw dicts.
    """

    field_name: str = Field(
        description="The name of the model field this node maps to."
    )
    value: Any = Field(description="The extracted value, typed according to the model.")
    marker: Marker = Field(description="The structured marker that produced this data.")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional handler-specific metadata."
    )


class RenderContext(BaseModel):
    """
    Contract for the data passed to the renderer.
    """

    model_name: str = Field(
        description="The name of the Pydantic model being rendered."
    )
    data: dict[str, Any] = Field(
        description="The structured data to be injected into the template."
    )
    template_path: str | None = Field(
        default=None, description="Optional path to the source template."
    )
