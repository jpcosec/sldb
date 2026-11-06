"""Gramatica de una paleta: hex de fondos, ink y tokens, y nombres de icono."""

from __future__ import annotations

from sldb.notations.errors.invalid_color_error import InvalidColorError
from sldb.notations.errors.unknown_icon_error import UnknownIconError
from sldb.notations.palette_constants import HEX, ICON_NAME, THEMES
from sldb.notations.palette_spec import PaletteSpec


def _check_theme_hex(palette: PaletteSpec) -> None:
    for theme in THEMES:
        for what, color in (("backgrounds", palette.backgrounds), ("ink", palette.ink)):
            value = getattr(color, theme)
            if not HEX.match(value):
                raise InvalidColorError(f"palette {palette.name}: {what}.{theme} {value!r} is not a `#rrggbb` hex")


def _check_token_hex(palette: PaletteSpec) -> None:
    for token, color in palette.colors.items():
        for theme in THEMES:
            if not HEX.match(getattr(color, theme)):
                raise InvalidColorError(f"palette {palette.name}: token {token!r}.{theme} {getattr(color, theme)!r} is not a `#rrggbb` hex")


def _check_icon_names(palette: PaletteSpec) -> None:
    for icon in palette.icon_set.icons:
        if not ICON_NAME.match(icon):
            raise UnknownIconError(f"palette {palette.name}: icon {icon!r} is not a {palette.icon_set.name} icon name (kebab-case, no URLs)")


def check_palette_grammar(palette: PaletteSpec) -> None:
    """Hex validos en fondos, ink y tokens, y nombres de icono bien formados."""
    _check_theme_hex(palette)
    _check_token_hex(palette)
    _check_icon_names(palette)
