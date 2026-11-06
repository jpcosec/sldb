"""`GlyphDoc` del vocabulario visual y la proyeccion."""

from __future__ import annotations

from pydantic import Field
from sldb.models.structured_nl_doc import StructuredNLDoc


class GlyphDoc(StructuredNLDoc):
    """Como se ve un documento: un modelo (y un predicado) -> forma, rotulo, compartimentos."""

    __semantics__ = {
        "type": ["notation", "glyph"],
        "layer": ["presentation"],
        "system": ["spec2viz"],
    }
    __references__ = ["notation"]
    __template__ = """---
id: ⸢rev•id⸥
notation: ⸢optrev•notation⸥
model: ⸢rev•model⸥
where: ⸢rev•where⸥
shape: ⸢rev•shape⸥
label: ⸢rev•label⸥
label_style: ⸢rev•label_style⸥
keyword: ⸢rev•keyword⸥
compartments: ⸢rev,list•compartments⸥
function: ⸢rev•function⸥
form: ⸢rev•form⸥
kind: ⸢optrev•kind⸥
fill: ⸢optrev•fill⸥
stroke: ⸢optrev•stroke⸥
icon: ⸢optrev•icon⸥
---

# ⸢rev•title⸥

## Description

⸢rev,markdown•description⸥
""".strip()

    id: str = Field(description="`<notation>.<glyph>`; nombre del documento.")
    title: str = Field(description="Nombre legible del glifo.")
    notation: str = Field(description="Id `NotationDoc:<name>` de la notacion a la que pertenece.")
    model: str = Field(description="Modelo del store cuyos documentos dibuja (SpecNodeDoc, ClassDoc...).")
    where: str = Field(default="", description="Predicado sobre el payload, en la gramatica de `sldb find --where`; vacio casa con todo.")
    shape: str = Field(description="Forma primitiva de la superficie (class-box, rounded-box, rounded-container, bullseye...).")
    label: str = Field(default="{title}", description="Plantilla del rotulo; `{campo}` lee del payload del documento.")
    label_style: str = Field(default="", description="Estilo del rotulo (italic, bold) o vacio.")
    keyword: str = Field(default="", description="Estereotipo o palabra clave encima del rotulo (`«interface»`).")
    compartments: list[str] = Field(default_factory=list, description="Campos del payload que se muestran como compartimentos, en orden (`data.attributes`).")
    function: str = Field(default="", description="Papel semantico del glifo en la notacion (class, interface, state, terminal).")
    form: str = Field(default="", description="Forma pron equivalente al par model/where, si alguien la interpreta; spec2viz no.")
    kind: str | None = Field(default=None, description="Kind de la paleta cuya forma de referencia, icono y colores toma el glifo.")
    fill: str | dict | None = Field(default=None, description="Relleno: token de la paleta, `#rrggbb` (el mismo en los dos temas) o `{light, dark}`.")
    stroke: str | dict | None = Field(default=None, description="Trazo: token de la paleta, `#rrggbb` o `{light, dark}`.")
    icon: str | None = Field(default=None, description="Icono del set declarado por la paleta (Lucide, kebab-case).")
    description: str = Field(default="", description="Texto libre.")
