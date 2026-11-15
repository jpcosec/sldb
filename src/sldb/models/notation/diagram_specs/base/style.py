"""`Style`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

class Style(BaseModel):
    model_config = ConfigDict(extra="forbid")

    theme: str = Field(
        default="default",
        description="Renderer theme name used to style the generated output.",
    )
    kinds: dict[str, dict] = Field(
        default_factory=dict,
        description=(
            "Style per semantic kind. Neutral keys `fill`, `stroke` (a token of the default palette such as "
            "`database-fill`, a `#rrggbb` hex used in both themes, or a `{light, dark}` pair of hex or tokens) and "
            "`icon` (a name of the palette's Lucide icon set) apply to every "
            "renderer and to graph_ui, below the notation's glyph and above the default palette. A renderer-specific "
            "block (such as `plantuml: {background, border, font}`) is read only by that renderer."
        ),
    )
