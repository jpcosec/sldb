"""Carga de paletas: builtin por nombre o YAML propio, validadas."""

from __future__ import annotations

from pathlib import Path

import yaml

from sldb.notations.errors.validation_error import ValidationError
from sldb.notations.palette_checks import check_palette
from sldb.notations.palette_constants import DEFAULT_PALETTE, PALETTES_DIR
from sldb.notations.palette_spec import PaletteSpec


def builtin_palettes() -> dict[str, Path]:
    return {p.stem: p for p in sorted(PALETTES_DIR.glob("*.yml"))}


def resolve_palette(name_or_path: str | Path, base: Path | None = None) -> Path:
    """La ruta de una paleta: un nombre builtin o un YAML propio (relativo a `base` si se da)."""
    text = str(name_or_path)
    builtin = builtin_palettes()
    if text in builtin:
        return builtin[text]
    path = Path(text)
    if not path.is_absolute() and base is not None:
        path = base / path
    if path.is_file():
        return path.resolve()
    raise ValidationError(f"unknown palette {text!r}: not a builtin ({', '.join(builtin) or 'none'}) nor a file")


def _read_yaml(path: Path) -> dict:
    """El YAML de una paleta; `ValidationError` si no parsea."""
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise ValidationError(f"{path}: invalid YAML: {exc}") from exc


def load_palette(name_or_path: str | Path = DEFAULT_PALETTE, base: Path | None = None) -> PaletteSpec:
    """Carga y valida una paleta; errores tipados si no es valida."""
    path = resolve_palette(name_or_path, base)
    try:
        palette = PaletteSpec.model_validate(_read_yaml(path))
    except ValueError as exc:
        raise ValidationError(f"{path}: {exc}") from exc
    check_palette(palette)
    return palette


def palette_ref(name: str) -> str:
    return f"PaletteDoc:{name}"
