"""Resolucion de colores: token, hex o par `{light, dark}` a `{light, dark}`."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from sldb.notations.errors.invalid_color_error import InvalidColorError
from sldb.notations.palette_constants import HEX


def _resolve_pair(value: dict, tokens: dict[str, Any], where: str) -> dict[str, str]:
    """Un par cuyos lados son cada uno un hex o un token."""
    if set(value) != {"light", "dark"}:
        at = f"{where}: " if where else ""
        raise InvalidColorError(f"{at}a color pair takes exactly `light` and `dark`, got {sorted(value)}")
    return {theme: resolve_color(value[theme], tokens, f"{where} {theme}".strip())[theme] for theme in ("light", "dark")}


def _token_pair(token: Any) -> dict[str, str]:
    """El `{light, dark}` en minusculas de un token."""
    token = token.model_dump() if isinstance(token, BaseModel) else dict(token)
    return {"light": str(token["light"]).lower(), "dark": str(token["dark"]).lower()}


def resolve_color(value: "str | dict[str, str]", tokens: dict[str, Any], where: str = "") -> dict[str, str]:
    """Un color como `{light, dark}`: token de la paleta, hex `#rrggbb` o par `{light, dark}`."""
    if isinstance(value, dict):
        return _resolve_pair(value, tokens, where)
    text = str(value or "").strip()
    if HEX.match(text):
        return {"light": text.lower(), "dark": text.lower()}
    if text in tokens:
        return _token_pair(tokens[text])
    at = f"{where}: " if where else ""
    raise InvalidColorError(f"{at}color {text!r} is neither a `#rrggbb` hex nor a palette token ({', '.join(sorted(tokens)) or 'none'})")
