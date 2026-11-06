"""`NotationDoc` del vocabulario visual y la proyeccion."""

from __future__ import annotations

from pydantic import Field
from sldb.models.structured_doc import StructuredNLDoc


class NotationDoc(StructuredNLDoc):
    """Una notacion: nivel, tipo de diagrama, layout y los glifos y links que la componen."""

    __semantics__ = {
        "type": ["notation", "vocabulary"],
        "layer": ["presentation"],
        "system": ["spec2viz"],
    }
    __references__ = ["glyphs", "links", "palette"]
    __template__ = """---
id: ⸢rev•id⸥
name: ⸢rev•name⸥
diagram_type: ⸢rev•diagram_type⸥
level: ⸢rev•level⸥
projection: ⸢rev•projection⸥
layout: ⸢rev•layout⸥
markers: ⸢rev•markers⸥
glyphs: ⸢rev,list•glyphs⸥
links: ⸢rev,list•links⸥
palette: ⸢optrev•palette⸥
---

# ⸢rev•title⸥

## Description

⸢rev,markdown•description⸥
""".strip()

    id: str = Field(description="Nombre de la notacion; nombre del documento (`NotationDoc:<name>`).")
    title: str = Field(description="Titulo legible de la notacion.")
    name: str = Field(description="Nombre de la notacion, igual al id.")
    diagram_type: str = Field(description="Tipo de diagrama al que aplica (class, state, component...).")
    level: str = Field(default="types", description="Nivel que dibuja: `types`, `instances` o `both`.")
    projection: str = Field(default="all", description="Proyeccion del store sobre la que se dibuja; `all` sin filtro.")
    layout: dict = Field(default_factory=dict, description="Layout de la vista: `kind` (graph, tree, lanes, grid, axis) y sus parametros (direction...).")
    markers: list[dict] = Field(
        default_factory=list,
        description="Marcas que apuntan a un elemento sin ser su glifo (el pseudoestado inicial): `id`, `shape`, `model`, `where`.",
    )
    glyphs: list[str] = Field(default_factory=list, description="Ids `GlyphDoc:<notation>.<glyph>` en orden de prioridad: el primero que casa gana.")
    links: list[str] = Field(default_factory=list, description="Ids `LinkDoc:<notation>.<link>`.")
    palette: str | None = Field(default=None, description="Id `PaletteDoc:<name>` de la paleta que usa; ausente si la notacion no usa estilo.")
    description: str = Field(default="", description="Que dibuja la notacion y sobre que mundo.")
