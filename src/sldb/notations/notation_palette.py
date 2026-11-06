"""`notation_palette`: la paleta que usa una notacion."""

from __future__ import annotations

from pathlib import Path

from sldb.notations.notation_spec import NotationSpec
from sldb.notations.palette_constants import DEFAULT_PALETTE
from sldb.notations.palette_files import load_palette


def notation_palette(notation: NotationSpec, base: Path | None = None):
    """La paleta que usa una notacion (`PaletteSpec`), o None si no usa estilo."""
    if not notation.styled:
        return None
    return load_palette(notation.palette or DEFAULT_PALETTE, base)
