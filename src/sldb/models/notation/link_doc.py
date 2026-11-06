"""`LinkDoc` del vocabulario visual y la proyeccion."""

from __future__ import annotations

from pydantic import Field, field_validator
from sldb.models.structured_nl_doc import StructuredNLDoc


class LinkDoc(StructuredNLDoc):
    """Como se ve una relacion: linea, anidamiento, carril, celda o eje, con trazo y terminales."""

    __semantics__ = {
        "type": ["notation", "link"],
        "layer": ["presentation"],
        "system": ["spec2viz"],
    }
    __references__ = ["notation", "relation_type"]
    __template__ = """---
id: ⸢rev•id⸥
notation: ⸢optrev•notation⸥
relation: ⸢rev•relation⸥
relation_type: ⸢rev•relation_type⸥
model: ⸢rev•model⸥
draw: ⸢rev•draw⸥
line: ⸢rev•line⸥
source_end: ⸢rev•source_end⸥
target_end: ⸢rev•target_end⸥
label: ⸢rev•label⸥
source_label: ⸢optrev•source_label⸥
target_label: ⸢optrev•target_label⸥
ends: ⸢rev•ends⸥
form: ⸢rev•form⸥
color: ⸢optrev•color⸥
---

# ⸢rev•title⸥

## Description

⸢rev,markdown•description⸥
""".strip()

    id: str = Field(description="`<notation>.<link>`; nombre del documento.")
    title: str = Field(description="Nombre legible del link.")
    notation: str = Field(description="Id `NotationDoc:<name>` de la notacion a la que pertenece.")
    relation: str = Field(description="Nombre de la relacion del store que dibuja (`relation_type` de los RelationDoc).")
    relation_type: str = Field(description="Id `RelationTypeDoc:reltype-<relation>`; el indice lo convierte en arista hacia el tipo de relacion.")
    model: str = Field(default="", description="Modelo de la relacion reificada (un documento con extremos), si la hay; vacio si es una arista.")
    draw: str = Field(default="line", description="Como se dibuja: `line`, `nest`, `lane`, `cell` o `axis`.")
    line: str = Field(default="solid", description="Trazo de la linea: `solid`, `dashed`, `dotted`.")
    source_end: str = Field(default="none", description="Terminal en el origen (none, open-arrow, filled-arrow, hollow-triangle, hollow-diamond, filled-diamond, filled-circle, bar).")
    target_end: str = Field(default="open-arrow", description="Terminal en el destino.")
    label: str = Field(default="", description="Plantilla del rotulo sobre el payload del RelationDoc (`{notes}`).")
    source_label: str = Field(default="", description="Plantilla del rotulo junto al origen (`{from_multiplicity}`), sobre el payload y los `attributes` del RelationDoc.")
    target_label: str = Field(default="", description="Plantilla del rotulo junto al destino (`{to_multiplicity}`).")
    ends: dict = Field(default_factory=dict, description="Extremos de una relacion reificada: nombre -> {relation, label, terminal}.")
    form: str = Field(default="", description="Forma pron equivalente (`(relation R)`), si alguien la interpreta; spec2viz no.")
    color: str | dict | None = Field(default=None, description="Color de la linea: token de la paleta, `#rrggbb` o `{light, dark}`; ausente = el de la superficie.")
    description: str = Field(default="", description="Texto libre.")

    @field_validator("source_label", "target_label", mode="before")
    @classmethod
    def _absent_label(cls, value):
        return "" if value is None else value
