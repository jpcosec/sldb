"""Carga de notaciones: builtin por nombre o YAML propio, validadas, y sus ids en el store."""

from __future__ import annotations

from pathlib import Path

import yaml

from sldb.notations.errors.validation_error import ValidationError
from sldb.notations.notation_constants import NOTATIONS_DIR
from sldb.notations.notation_spec import NotationSpec
from sldb.notations.notation_style_check import check_notation_style


def builtin_notations() -> dict[str, Path]:
    """Las notaciones que sldb trae, por nombre."""
    return {p.stem: p for p in sorted(NOTATIONS_DIR.glob("*.yml"))}


def resolve_notation(name_or_path: str | Path) -> Path:
    """La ruta de una notacion: un nombre builtin o un YAML propio."""
    text = str(name_or_path)
    builtin = builtin_notations()
    if text in builtin:
        return builtin[text]
    path = Path(text)
    if path.is_file():
        return path.resolve()
    raise ValidationError(f"unknown notation {text!r}: not a builtin ({', '.join(builtin) or 'none'}) nor a file")


def _read_mapping(path: Path) -> dict:
    """El YAML de una notacion, que tiene que ser un mapa."""
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise ValidationError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValidationError(f"{path}: a notation is a mapping")
    return raw


def _style_checked(notation: NotationSpec, path: Path) -> None:
    """Valida el estilo de la notacion; el error lleva la ruta del archivo."""
    try:
        check_notation_style(notation, path.parent)
    except ValidationError as exc:
        raise type(exc)(f"{path}: {exc}") from exc


def load_notation(name_or_path: str | Path) -> NotationSpec:
    """Carga y valida una notacion; `ValidationError` (o una subclase tipada) si no es valida."""
    path = resolve_notation(name_or_path)
    try:
        notation = NotationSpec.model_validate(_read_mapping(path))
    except ValueError as exc:
        raise ValidationError(f"{path}: {exc}") from exc
    _style_checked(notation, path)
    return notation


def notation_ref(name: str) -> str:
    return f"NotationDoc:{name}"


def glyph_ref(notation: str, glyph_id: str) -> str:
    return f"GlyphDoc:{notation}.{glyph_id}"


def link_ref(notation: str, link_id: str) -> str:
    return f"LinkDoc:{notation}.{link_id}"
