"""Estilo de un elemento: precedencia glifo > `style.kinds` del spec > paleta, a `{light, dark}`."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from sldb.notations.color_resolution import resolve_color
from sldb.notations.palette_files import load_palette

PROPERTIES = ("fill", "stroke", "icon")


@lru_cache(maxsize=1)
def _builtin_default() -> dict[str, Any]:
    palette = load_palette()
    return {
        "name": palette.name,
        "colors": {k: v.model_dump() for k, v in palette.colors.items()},
        "kinds": {k: v.model_dump() for k, v in palette.kinds.items()},
        "icon_set": palette.icon_set.model_dump(),
        "ink": palette.ink.model_dump(),
    }


def _value(prop: str, raw: str, tokens: dict[str, Any], where: str) -> Any:
    if prop == "icon":
        return raw
    return resolve_color(raw, tokens, where)


def _layers(glyph: dict, kind: str, spec_kinds: dict | None, palette: dict | None) -> list[tuple[str, dict]]:
    """Las capas de estilo en orden de precedencia: glifo, kind del glifo, spec, paleta."""
    kinds = dict((palette or {}).get("kinds") or {})
    layers: list[tuple[str, dict]] = [("glyph", {p: glyph.get(p) for p in PROPERTIES})]
    if glyph.get("kind"):
        layers.append(("glyph", dict(kinds.get(glyph["kind"]) or _builtin_default()["kinds"].get(glyph["kind"]) or {})))
    if spec_kinds and kind in spec_kinds:
        layers.append(("spec", dict(spec_kinds[kind])))
    if palette is not None and kind in kinds:
        layers.append(("palette", dict(kinds[kind])))
    return layers


def _resolve_prop(prop: str, layers: list[tuple[str, dict]], tokens: dict[str, Any]):
    """`(valor, capa)` de la primera capa que define `prop`, o None."""
    for layer, values in layers:
        if values.get(prop):
            raw = values[prop] if isinstance(values[prop], dict) else str(values[prop])
            return _value(prop, raw, tokens, f"{layer} {prop}"), layer
    return None


def _resolve_all(layers: list[tuple[str, dict]], tokens: dict[str, Any]) -> dict[str, Any]:
    """Cada propiedad resuelta por la primera capa que la define, mas su `source`."""
    out: dict[str, Any] = {}
    source: dict[str, str] = {}
    for prop in PROPERTIES:
        found = _resolve_prop(prop, layers, tokens)
        if found:
            out[prop], source[prop] = found
    if out:
        out["source"] = source
    return out


def resolve_style(glyph: dict[str, Any] | None, kind: str, spec_kinds: dict[str, dict] | None,
                  palette: dict[str, Any] | None) -> dict[str, Any]:
    """`{fill, stroke, icon, source}` de un elemento; `source` dice de que capa salio cada una."""
    tokens = dict((palette or _builtin_default()).get("colors") or {})
    return _resolve_all(_layers(glyph or {}, kind, spec_kinds, palette), tokens)


def resolve_line_color(link: dict[str, Any] | None, palette: dict[str, Any] | None) -> dict[str, str] | None:
    """El color de la linea de un link (`{light, dark}`) o None si no lo define."""
    color = (link or {}).get("color")
    if not color:
        return None
    tokens = dict((palette or _builtin_default()).get("colors") or {})
    return resolve_color(color if isinstance(color, dict) else str(color), tokens, "link color")


__all__ = ["PROPERTIES", "resolve_style", "resolve_line_color"]
