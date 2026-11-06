"""`check_palette`: gramatica y accesibilidad de una paleta."""

from __future__ import annotations

from sldb.notations.palette_hex_checks import check_palette_grammar
from sldb.notations.palette_kind_checks import check_palette_kinds
from sldb.notations.palette_spec import PaletteSpec


def check_palette(palette: PaletteSpec) -> None:
    """Gramatica y accesibilidad de una paleta; errores tipados (`ValidationError` y subclases)."""
    check_palette_grammar(palette)
    check_palette_kinds(palette)
