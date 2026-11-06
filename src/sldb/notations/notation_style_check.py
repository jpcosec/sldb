"""`check_notation_style`: formas, kinds, colores e iconos de una notacion."""

from __future__ import annotations

from pathlib import Path

from sldb.notations.errors.unknown_icon_error import UnknownIconError
from sldb.notations.errors.unknown_kind_error import UnknownKindError
from sldb.notations.errors.unknown_shape_error import UnknownShapeError
from sldb.notations.glyph_spec import GlyphSpec
from sldb.notations.notation_constants import SHAPES
from sldb.notations.notation_palette import notation_palette
from sldb.notations.notation_spec import NotationSpec


def _check_shapes(notation: NotationSpec) -> None:
    for item in [*notation.glyphs, *notation.markers]:
        if item.shape not in SHAPES:
            what = "glyph" if isinstance(item, GlyphSpec) else "marker"
            raise UnknownShapeError(f"{what} {item.id!r}: shape {item.shape!r} is not one of {', '.join(SHAPES)}")


def _check_glyph(glyph: GlyphSpec, palette) -> None:
    where = f"glyph {glyph.id!r}"
    if glyph.kind and glyph.kind not in palette.kinds:
        raise UnknownKindError(f"{where}: kind {glyph.kind!r} is not in palette {palette.name} ({', '.join(palette.kinds)})")
    for field in ("fill", "stroke"):
        if getattr(glyph, field):
            palette.color(getattr(glyph, field), f"{where} {field}")
    if glyph.icon and glyph.icon not in palette.icon_set.icons:
        raise UnknownIconError(f"{where}: icon {glyph.icon!r} is not in the {palette.icon_set.name} icon set of palette {palette.name}")


def check_notation_style(notation: NotationSpec, base: Path | None = None) -> None:
    """Formas, kinds, colores e iconos de una notacion, con errores tipados:
    `UnknownShapeError`, `UnknownKindError`, `InvalidColorError`, `UnknownIconError`."""
    _check_shapes(notation)
    palette = notation_palette(notation, base)
    if palette is None:
        return
    for glyph in notation.glyphs:
        _check_glyph(glyph, palette)
    for link in notation.links:
        if link.color:
            palette.color(link.color, f"link {link.id!r} color")
