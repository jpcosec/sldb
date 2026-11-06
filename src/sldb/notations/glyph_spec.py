"""`GlyphSpec`: como se ve cada clase de elemento de una notacion."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from sldb.notations.notation_constants import _ID
from sldb.notations.where_check import _check_where


class GlyphSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str = ""
    model: str
    where: str = ""
    shape: str
    label: str = "{title}"
    label_style: str = ""
    keyword: str = ""
    compartments: list[str] = Field(default_factory=list)
    function: str = ""
    form: str = ""
    description: str = ""
    # estilo opcional (precedencia: glifo > Style.kinds del spec > paleta); un color es un token
    # de la paleta o `#rrggbb`, `kind` toma forma de referencia, icono y colores de la paleta
    kind: str = ""
    fill: str | dict[str, str] = ""    # token, `#rrggbb` (ambos temas) o `{light, dark}`
    stroke: str | dict[str, str] = ""
    icon: str = ""

    @field_validator("id")
    @classmethod
    def _id(cls, v: str) -> str:
        if not _ID.match(v):
            raise ValueError(f"glyph id {v!r} must match {_ID.pattern}")
        return v

    @field_validator("where")
    @classmethod
    def _where(cls, v: str) -> str:
        _check_where(v)
        return v
