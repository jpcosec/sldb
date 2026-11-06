"""Fachada de paletas: colores, forma e icono por defecto de los kinds comunes, como datos."""

from __future__ import annotations

from sldb.notations.color_resolution import resolve_color
from sldb.notations.icon_set import IconSet
from sldb.notations.kind_style import KindStyle
from sldb.notations.palette_checks import check_palette
from sldb.notations.palette_constants import (
    DEFAULT_PALETTE,
    HEX,
    ICON_NAME,
    MIN_GRAPHIC_CONTRAST,
    MIN_TEXT_CONTRAST,
    PALETTES_DIR,
    THEMES,
)
from sldb.notations.palette_files import builtin_palettes, load_palette, palette_ref, resolve_palette
from sldb.notations.palette_spec import PaletteSpec
from sldb.notations.theme_color import ThemeColor
from sldb.notations.wcag_contrast import contrast, luminance

__all__ = [
    "PaletteSpec", "KindStyle", "IconSet", "ThemeColor", "DEFAULT_PALETTE", "THEMES",
    "resolve_color", "contrast", "luminance", "check_palette",
    "builtin_palettes", "resolve_palette", "load_palette", "palette_ref",
    "PALETTES_DIR", "HEX", "ICON_NAME", "MIN_GRAPHIC_CONTRAST", "MIN_TEXT_CONTRAST",
]
