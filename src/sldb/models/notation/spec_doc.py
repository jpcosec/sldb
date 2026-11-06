"""`SpecDoc` del vocabulario visual y la proyeccion."""

from __future__ import annotations

from pydantic import Field, field_validator
from sldb.models.structured_doc import StructuredNLDoc


class SpecDoc(StructuredNLDoc):
    """Un spec de diagrama, como documento del store que contiene a sus nodos."""

    __semantics__ = {
        "type": ["architecture", "spec"],
        "layer": ["topology"],
        "system": ["spec2viz"],
    }
    # `references`, no `contains`: la relacion builtin `contains` es one_to_many y un nodo
    # anidado en otro ya tiene a ese otro como contenedor.
    __references__ = ["nodes", "notation"]
    __template__ = """---
id: ⸢rev•id⸥
diagram_type: ⸢rev•diagram_type⸥
version: ⸢rev•version⸥
spec_path: ⸢rev•spec_path⸥
sha256: ⸢rev•sha256⸥
notation: ⸢optrev•notation⸥
category: ⸢optrev•category⸥
nav: ⸢optrev•nav⸥
summary: ⸢optrev•summary⸥
style: ⸢optrev•style⸥
nodes: ⸢rev,list•nodes⸥
---

# ⸢rev•title⸥

## Description

⸢rev,markdown•description⸥
""".strip()

    id: str = Field(description="Id del spec (`id:` del YAML); nombre del documento.")
    title: str = Field(description="Titulo del spec, mostrado como H1.")
    diagram_type: str = Field(description="Tipo de diagrama del spec (component, sequence, state...).")
    version: str = Field(description="Version declarada en el spec.")
    spec_path: str = Field(description="Ruta del YAML relativa a la raiz del proyecto del store.")
    sha256: str = Field(description="SHA-256 del YAML en el momento de la sincronizacion.")
    nodes: list[str] = Field(
        default_factory=list,
        description="Ids `SpecNodeDoc:<spec>.<elemento>` de los nodos del spec; el indice los convierte en aristas `references`.",
    )
    notation: str = Field(
        default="",
        description="Id `NotationDoc:<name>` de la notacion con la que se dibuja el spec; vacio si no se asigno ninguna.",
    )
    category: str = Field(default="", description="Categoria del catalogo (`category` de vistas.yml); graph_ui agrupa los specs por ella.")
    nav: str = Field(default="", description="Rotulo corto de navegacion del catalogo (`nav` de vistas.yml).")
    summary: str = Field(default="", description="Resumen del catalogo (`desc` de vistas.yml).")
    style: dict | None = Field(
        default=None,
        description="`style.kinds` neutral del spec (kind -> fill, stroke, icon): segundo nivel de la precedencia de estilo (glifo > spec > paleta); ausente si el spec no lo declara.",
    )
    description: str = Field(default="", description="Descripcion del spec (`metadata.description` del YAML).")

    @field_validator("notation", "category", "nav", "summary", mode="before")
    @classmethod
    def _absent_text(cls, value):
        # un documento escrito antes de que el campo existiera se extrae como None
        return "" if value is None else value
