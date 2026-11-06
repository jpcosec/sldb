"""`PaletteSpec`: una paleta completa, tal como esta en su YAML."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.notations.color_resolution import resolve_color
from sldb.notations.icon_set import IconSet
from sldb.notations.kind_style import KindStyle
from sldb.notations.theme_color import ThemeColor


class PaletteSpec(BaseModel):
    """Una paleta completa, tal como esta en su YAML."""

    model_config = ConfigDict(extra="forbid")

    name: str
    title: str = ""
    backgrounds: ThemeColor
    ink: ThemeColor
    icon_set: IconSet
    colors: dict[str, ThemeColor] = Field(default_factory=dict)
    kinds: dict[str, KindStyle] = Field(default_factory=dict)
    description: str = ""

    def color(self, value: str, where: str = "") -> dict[str, str]:
        """Un token o un hex -> `{light, dark}`; `InvalidColorError` si no es ninguno."""
        return resolve_color(value, self.colors, where)
