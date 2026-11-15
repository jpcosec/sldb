"""`validate_style`: los colores e iconos de `style.kinds`."""

from __future__ import annotations

from sldb.models.notation.diagram_specs.base.base_diagram import BaseDiagram
from sldb.notations.exceptions import UnknownIconError
from sldb.notations.color_resolution import resolve_color
from sldb.notations.styling import _builtin_default

def _check_colors(d_id: str, kind: str, entry: dict, default: dict) -> None:
    for prop in ("fill", "stroke"):
        if entry.get(prop):
            value = entry[prop] if isinstance(entry[prop], dict) else str(entry[prop])
            resolve_color(value, default["colors"], f"{d_id} style.kinds.{kind}.{prop}")


def _check_icon(d_id: str, kind: str, entry: dict, default: dict) -> None:
    if entry.get("icon") and str(entry["icon"]) not in default["icon_set"]["icons"]:
        raise UnknownIconError(f"{d_id} style.kinds.{kind}.icon {entry['icon']!r} is not in the {default['icon_set']['name']} icon set")


def validate_style(d: BaseDiagram) -> None:
    """`style.kinds` neutral (fill, stroke, icon): colores token de la paleta default o `#rrggbb`
    (`InvalidColorError`), iconos del set declarado (`UnknownIconError`). Las claves de un
    renderer (como `plantuml`) no se validan aqui."""
    if d.style is None or not d.style.kinds:
        return
    default = _builtin_default()
    for kind, entry in d.style.kinds.items():
        if isinstance(entry, dict):
            _check_colors(d.id, kind, entry, default)
            _check_icon(d.id, kind, entry, default)
