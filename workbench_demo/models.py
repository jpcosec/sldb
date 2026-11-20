from __future__ import annotations
from pydantic import Field
from sldb import StructuredNLDoc

class FuenteDoc(StructuredNLDoc):
    """Documento de fuente original de solo lectura."""
    __authority__ = "source_raw"
    __template__ = """# ⸢rev•title⸥

Fecha: ⸢rev•fecha⸥
Autor: ⸢rev•autor⸥

## Contenido

⸢rev•texto⸥
""".strip()
    title: str = Field(description="Título de la fuente.")
    fecha: str = Field(description="Fecha de emisión.")
    autor: str = Field(description="Entidad o autor emisor.")
    texto: str = Field(description="Texto original transcrito.")


class AtomDoc(StructuredNLDoc):
    """Átomo de conocimiento estructurado justificativo."""
    __authority__ = "authored"
    __semantics__ = {"type": ["clinical", "atom"]}
    __template__ = """# ⸢rev•title⸥

Estado: ⸢rev•estado⸥
Autor: ⸢rev•autor⸥
Fuente: ⸢rev•fuente_ref⸥

## Cuerpo

⸢rev•cuerpo⸥
""".strip()
    title: str = Field(description="Título o resumen del criterio.")
    estado: str = Field(default="aprobado", description="Estado de confirmación.")
    autor: str = Field(default="Dr. Valenzuela", description="Autor del átomo.")
    fuente_ref: str = Field(default="", description="Referencia a FuenteDoc.")
    cuerpo: str = Field(description="Enunciado canónico del criterio.")


class InformeDoc(StructuredNLDoc):
    """Documento raíz de informe clínico con transclusiones y diagramas."""
    __authority__ = "authored"
    __semantics__ = {"domain": ["clinical", "protocol"]}
    __containment__ = {"criterios": ["AtomDoc"]}
    __references__ = ["criterios", "decision_spec", "fuente_ref"]
    __compositions__ = {
        "criterios_transcluidos": {
            "source_field": "criterios",
            "ref": "field",
            "template": "⸢field•{field}⸥",
        }
    }
    __template__ = """# ⸢rev•title⸥

Versión: ⸢rev•version⸥
Fuente: ⸢rev•fuente_ref⸥

## Objetivo y Contexto Clínico

⸢rev•objetivo⸥

## Criterios de Selección y Exclusión

- ⸢rev,list•criterios⸥

## Diagrama de Decisión Renal

⸢rev,diagram•decision_spec⸥

## Matriz de Ajuste Basal por Cohorte

⸢rev,table[cohorte,imc,ajuste,origen_ref]•tabla_dosis⸥

## Tolerancia y Hallazgos Secundarios

⸢rev•tolerancia⸥
""".strip()
    title: str = Field(description="Título del informe.")
    version: str = Field(default="v2.4.1", description="Versión de publicación.")
    fuente_ref: str = Field(default="FuenteDoc:acta-comite-01", description="Fuente primaria.")
    objetivo: str = Field(description="Objetivo clínico del informe.")
    criterios: list[str] = Field(default_factory=list, description="Lista de referencias a átomos.")
    decision_spec: str = Field(description="Referencia a SpecDoc o ViewDoc.")
    tabla_dosis: list[dict[str, str]] = Field(default_factory=list, description="Matriz de dosis estructurada.")
    tolerancia: str = Field(description="Notas de tolerancia y hallazgos.")
