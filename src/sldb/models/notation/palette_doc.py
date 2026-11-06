"""`PaletteDoc` del vocabulario visual y la proyeccion."""

from __future__ import annotations

from pydantic import Field
from sldb.models.structured_doc import StructuredNLDoc


class PaletteDoc(StructuredNLDoc):
    """Una paleta: fondos e ink por tema, set de iconos, tokens de color y estilo por kind."""

    __semantics__ = {
        "type": ["palette", "vocabulary"],
        "layer": ["presentation"],
        "system": ["spec2viz"],
    }
    __template__ = """---
id: ⸢rev•id⸥
name: ⸢rev•name⸥
backgrounds: ⸢rev•backgrounds⸥
ink: ⸢rev•ink⸥
icon_set: ⸢rev•icon_set⸥
colors: ⸢rev•colors⸥
kinds: ⸢rev•kinds⸥
---

# ⸢rev•title⸥

## Description

⸢rev,markdown•description⸥
""".strip()

    id: str = Field(description="Nombre de la paleta; nombre del documento (`PaletteDoc:<name>`).")
    name: str = Field(description="Nombre de la paleta, igual al id.")
    title: str = Field(description="Titulo legible.")
    backgrounds: dict = Field(description="Fondo de cada tema: `{light, dark}` en `#rrggbb`.")
    ink: dict = Field(description="Color del texto en cada tema: `{light, dark}`.")
    icon_set: dict = Field(description="Set de iconos declarado: `{name, version, icons}`; solo esos nombres son validos.")
    colors: dict = Field(default_factory=dict, description="Tokens de color: nombre -> `{light, dark}`.")
    kinds: dict = Field(default_factory=dict, description="Estilo por kind: `{shape, icon, fill, stroke}` con colores como tokens.")
    description: str = Field(default="", description="Texto libre.")
