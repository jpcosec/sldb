"""Accesibilidad y unicidad de los kinds de una paleta."""

from __future__ import annotations

from sldb.notations.errors.unknown_icon_error import UnknownIconError
from sldb.notations.errors.unknown_shape_error import UnknownShapeError
from sldb.notations.errors.validation_error import ValidationError
from sldb.notations.kind_style import KindStyle
from sldb.notations.notation_constants import SHAPES
from sldb.notations.palette_constants import MIN_GRAPHIC_CONTRAST, MIN_TEXT_CONTRAST, THEMES
from sldb.notations.palette_spec import PaletteSpec
from sldb.notations.wcag_contrast import contrast


def _check_shape_icon(palette: PaletteSpec, style: KindStyle, where: str) -> None:
    if style.shape not in SHAPES:
        raise UnknownShapeError(f"{where}: shape {style.shape!r} is not one of {', '.join(SHAPES)}")
    if style.icon not in palette.icon_set.icons:
        raise UnknownIconError(f"{where}: icon {style.icon!r} is not in the {palette.icon_set.name} icon set")


def _check_theme_contrast(palette: PaletteSpec, theme: str, where: str, fill: dict, stroke: dict) -> None:
    background, ink = getattr(palette.backgrounds, theme), getattr(palette.ink, theme)
    if contrast(stroke[theme], background) < MIN_GRAPHIC_CONTRAST:
        raise ValidationError(f"{where}: stroke {stroke[theme]} contrasts {contrast(stroke[theme], background):.2f}:1 with the {theme} background {background}; WCAG 1.4.11 needs {MIN_GRAPHIC_CONTRAST}:1")
    if contrast(ink, fill[theme]) < MIN_TEXT_CONTRAST:
        raise ValidationError(f"{where}: text {ink} on fill {fill[theme]} ({theme}) contrasts {contrast(ink, fill[theme]):.2f}:1; WCAG AA needs {MIN_TEXT_CONTRAST}:1")


def _check_pair(where: str, kind: str, style: KindStyle, pairs: dict[tuple[str, str], str]) -> None:
    pair = (style.shape, style.icon)
    if pair in pairs:
        raise ValidationError(f"{where}: shape and icon {pair} repeat kind {pairs[pair]!r}; colour must not be the only cue")
    pairs[pair] = kind


def _check_kind(palette: PaletteSpec, kind: str, style: KindStyle, pairs: dict[tuple[str, str], str]) -> None:
    where = f"palette {palette.name}, kind {kind}"
    _check_shape_icon(palette, style, where)
    fill, stroke = palette.color(style.fill, where), palette.color(style.stroke, where)
    for theme in THEMES:
        _check_theme_contrast(palette, theme, where, fill, stroke)
    _check_pair(where, kind, style, pairs)


def check_palette_kinds(palette: PaletteSpec) -> None:
    """Formas, iconos, contraste WCAG y par (forma, icono) distinto por kind."""
    pairs: dict[tuple[str, str], str] = {}
    for kind, style in palette.kinds.items():
        _check_kind(palette, kind, style, pairs)
