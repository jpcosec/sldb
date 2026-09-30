from __future__ import annotations
from typing import Literal
from pydantic import Field
from sldb import StructuredNLDoc


class ActaDoc(StructuredNLDoc):
    __template__ = """
# ⸢rev•title⸥

⸢rev,markdown•body⸥
""".strip()
    title: str = Field(description="Titulo del acta.")
    body: str = Field(description="Texto fuente completo.")


class AtomDoc(StructuredNLDoc):
    __semantics__ = {"type": ["knowledge", "atom"]}
    __references__ = ["source"]
    __template__ = """
---
kind: ⸢rev•kind⸥
status: ⸢rev•status⸥
source: ⸢rev•source⸥
start: ⸢rev•start⸥
end: ⸢rev•end⸥
tags: ⸢rev•tags⸥
---

# ⸢rev•text⸥

> ⸢rev•quote⸥
""".strip()
    kind: Literal["entidad", "hecho", "decision", "pendiente", "riesgo"] = Field(description="Tipo de atomo.")
    status: Literal["propuesto", "confirmado"] = Field(default="propuesto", description="Revision humana.")
    source: str = Field(description="Id del documento fuente: Model:name.")
    start: int = Field(description="Offset inicial del ancla en el texto del campo body.")
    end: int = Field(description="Offset final (exclusivo).")
    tags: list[str] = Field(default_factory=list, description="Tags de grupo.")
    text: str = Field(description="El hecho, en una linea.")
    quote: str = Field(description="Cita literal del ancla; permite detectar drift.")


class InformeDoc(StructuredNLDoc):
    __compositions__ = {
        "decisiones": {"source_field": "decisiones", "model": "models:AtomDoc",
                       "template": "- {text}", "separator": "\n"},
    }
    __template__ = """
# ⸢rev•title⸥

## Decisiones

⸢render•decisiones⸥
""".strip()
    title: str = Field(description="Titulo del informe.")
    decisiones: list[str] = Field(default_factory=list, description="Rutas de atomos.")
