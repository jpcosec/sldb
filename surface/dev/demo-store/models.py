"""Modelos de la tienda demo de la superficie: cubre libre, estructurado y composición."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from sldb import StructuredNLDoc


class NotaDoc(StructuredNLDoc):
    __template__ = "⸢rev•body⸥"

    body: str = Field(description="Texto libre en Markdown; el documento completo es este campo.")


class DecisionDoc(StructuredNLDoc):
    __template__ = """
---
status: ⸢rev•status⸥
owner: ⸢rev•owner⸥
review: ⸢optrev•review⸥
---

# ⸢rev•title⸥

**Sistema:** ⸢rev•system⸥

## Contexto

⸢rev•context⸥

## Decisión

⸢rev•decision⸥

## Etiquetas

- ⸢rev,list•tags⸥

## Alternativas

⸢rev,table[opcion,motivo]•alternatives⸥
""".strip()

    status: Literal["propuesta", "aceptada", "descartada"] = Field(description="Estado de la decisión en el ciclo de acuerdos.")
    owner: str = Field(description="Persona responsable de confirmar la decisión.")
    review: str | None = Field(default=None, description="Fecha de revisión pactada, si existe.")
    title: str = Field(description="Enunciado corto de la decisión, se lee como título.")
    system: str = Field(description="Sistema o frente al que aplica la decisión.")
    context: str = Field(description="Por qué hubo que decidir: restricción o hecho que la origina.")
    decision: str = Field(description="Qué se decidió, en Markdown.")
    tags: list[str] = Field(default_factory=list, description="Etiquetas semánticas para agrupar decisiones.")
    alternatives: list[dict[str, str]] = Field(default_factory=list, description="Alternativas evaluadas y por qué se descartaron.")


class AcuerdosDoc(StructuredNLDoc):
    __compositions__ = {
        "decisiones_compuestas": {
            "source_field": "decisiones",
            "model": "models:DecisionDoc",
            "template": "### {title}\n\n{decision}",
            "separator": "\n\n",
        }
    }
    __template__ = """
# ⸢rev•title⸥

⸢rev•intro⸥

## Decisiones incluidas

- ⸢rev,list•decisiones⸥

## Detalle

⸢render•decisiones_compuestas⸥
""".strip()

    title: str = Field(description="Título del documento de acuerdos.")
    intro: str = Field(description="Párrafo introductorio del documento compuesto.")
    decisiones: list[str] = Field(default_factory=list, description="Rutas de las decisiones que este documento compone, en orden.")
