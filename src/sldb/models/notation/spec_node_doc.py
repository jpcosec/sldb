"""`SpecNodeDoc` del vocabulario visual y la proyeccion."""

from __future__ import annotations

from pydantic import Field, field_validator
from sldb.models.structured_nl_doc import StructuredNLDoc


class SpecNodeDoc(StructuredNLDoc):
    """Un elemento de un spec de diagrama (nodo, estado, paso, clase, participante) como documento."""

    __semantics__ = {
        "type": ["architecture", "spec", "node"],
        "layer": ["topology"],
        "system": ["spec2viz"],
    }
    __references__ = ["spec", "refs", "atom_refs"]
    __containment__ = {"contains": ["SpecNodeDoc"]}
    __template__ = """---
id: ⸢rev•id⸥
spec: ⸢rev•spec⸥
element: ⸢rev•element⸥
kind: ⸢rev•kind⸥
collection: ⸢optrev•collection⸥
refs: ⸢rev,list•refs⸥
atom_refs: ⸢rev,list•atom_refs⸥
contains: ⸢rev,list•contains⸥
data: ⸢optrev•data⸥
---

# ⸢rev•title⸥

## Description

⸢rev,markdown•description⸥
""".strip()

    id: str = Field(description="`<spec id>.<element id>`; nombre del documento.")
    title: str = Field(description="Etiqueta del elemento en el diagrama (o su id si no tiene).")
    spec: str = Field(description="Id `SpecDoc:<spec id>` del spec al que pertenece el elemento.")
    element: str = Field(description="Id del elemento dentro del spec.")
    kind: str = Field(default="", description="`kind` del elemento en el spec, si lo declara.")
    collection: str = Field(default="", description="Coleccion del spec de la que sale el elemento (nodes, artifacts, states, steps, participants, classes, components, stages).")
    refs: list[str] = Field(
        default_factory=list,
        description="`refs:` del elemento: ids `Model:name` (o `store:Model:name`) de documentos que el nodo apunta.",
    )
    atom_refs: list[str] = Field(
        default_factory=list,
        description="`atoms:` del elemento, como ids `AtomDoc:<atom id>`.",
    )
    contains: list[str] = Field(
        default_factory=list,
        description="Ids `SpecNodeDoc:<spec>.<elemento>` de los elementos anidados (`contains:` del spec).",
    )
    data: dict = Field(
        default_factory=dict,
        description="El resto del elemento tal como esta en el spec (attributes, methods, guard, initial...); los compartimentos de un GlyphDoc leen de aqui.",
    )
    description: str = Field(default="", description="Texto libre del elemento, si el spec lo trae.")

    @field_validator("data", mode="before")
    @classmethod
    def _absent_data(cls, value):
        return {} if value is None else value

    @field_validator("collection", mode="before")
    @classmethod
    def _absent_collection(cls, value):
        return "" if value is None else value
