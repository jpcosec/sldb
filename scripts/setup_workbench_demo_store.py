#!/usr/bin/env python3
"""Configura un store SLDB real con los modelos y datos del mock de UI Workbench.

Crea:
- workbench_demo/
  - models.py (FuenteDoc, AtomDoc, InformeDoc)
  - .sldb/ (store inicializado, índices, edge index)
  - Documentos reales en markdown/yaml con transclusiones vivas y diagramas.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Asegurar sldb en sys.path
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "sldb" / "src"))

from pydantic import Field
from sldb import StructuredNLDoc, api
from sldb.api.segments import FieldRefResolver, build_document_segments
from sldb.models.notation_models import (
    GlyphDoc,
    LinkDoc,
    NotationDoc,
    PaletteDoc,
    SpecDoc,
    SpecNodeDoc,
    ViewDoc,
)


def create_demo_models_file(models_path: Path):
    """Escribe los modelos en workbench_demo/models.py."""
    content = '''from __future__ import annotations
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
'''
    models_path.write_text(content, encoding="utf-8")


def main():
    demo_dir = REPO_ROOT / "workbench_demo"
    demo_dir.mkdir(parents=True, exist_ok=True)

    models_file = demo_dir / "models.py"
    create_demo_models_file(models_file)

    pythonpath = str(REPO_ROOT)

    # 1. Inicializar store SLDB
    print(f"[*] Inicializando store en {demo_dir}...")
    store_loc = api.init_store(demo_dir)
    store_path = store_loc.store_path
    api.init_relations(store_path)

    # 2. Registrar modelos
    print("[*] Registrando modelos...")
    # Builtin notations
    for model_name in ["SpecDoc", "SpecNodeDoc", "NotationDoc", "GlyphDoc", "LinkDoc", "PaletteDoc", "ViewDoc"]:
        api.add_model(store_path, f"sldb.models.notation_models:{model_name}", pythonpath=pythonpath)

    # Modelos del demo
    api.add_model(store_path, "workbench_demo.models:FuenteDoc", pythonpath=pythonpath)
    api.add_model(store_path, "workbench_demo.models:AtomDoc", pythonpath=pythonpath)
    api.add_model(store_path, "workbench_demo.models:InformeDoc", pythonpath=pythonpath)

    # 3. Sincronizar notaciones builtin
    print("[*] Sincronizando paleta default y notación activity...")
    api.sync_palette(store_path, "default")
    api.sync_notation(store_path, "activity")

    # 4. Crear documentos de prueba
    print("[*] Creando documentos...")

    # FuenteDoc: acta-comite-01
    fuente_text = (
        "Reunión extraordinaria del Comité de Farmacología Clínica realizada el 12 de Octubre de 2026. "
        "Se revisan los protocolos de heparina y levira en pacientes con compromiso renal agudo. "
        "Acuerdo 1: Se considerará causal inmediata de exclusión un clearance de creatinina < 30 mL/min medido en dos tomas. "
        "Acuerdo 2: En insuficiencia hepática Child-Pugh B, la titulación inicial se reducirá al 50%. "
        "Acuerdo 3: Para cohortes con IMC < 18.5 se aplicará reducción de titulación basal del 25%."
    )
    api.create_document(
        store_path,
        "FuenteDoc",
        demo_dir / "acta-comite-01.md",
        {
            "title": "Acta Comité 01",
            "fecha": "2026-10-12",
            "autor": "Comité Ético-Farmacológico Central",
            "texto": fuente_text,
        },
        name="acta-comite-01",
        pythonpath=pythonpath,
    )

    # AtomDoc: atom-04, atom-05, atom-07
    api.create_document(
        store_path,
        "AtomDoc",
        demo_dir / "atom-04.md",
        {
            "title": "Criterio de exclusión renal",
            "estado": "confirmado",
            "autor": "Dr. Valenzuela",
            "fuente_ref": "FuenteDoc:acta-comite-01",
            "cuerpo": "Se considerará causal inmediata de exclusión un clearance de creatinina < 30 mL/min medido en dos tomas separadas por 48 horas.",
        },
        name="atom-04",
        pythonpath=pythonpath,
    )

    api.create_document(
        store_path,
        "AtomDoc",
        demo_dir / "atom-05.md",
        {
            "title": "Dosificación en insuficiencia hepática",
            "estado": "confirmado",
            "autor": "Dra. Soto",
            "fuente_ref": "FuenteDoc:acta-comite-01",
            "cuerpo": "Pacientes con Child-Pugh B requieren ajuste de titulación inicial al 50%.",
        },
        name="atom-05",
        pythonpath=pythonpath,
    )

    api.create_document(
        store_path,
        "AtomDoc",
        demo_dir / "atom-07.md",
        {
            "title": "Criterio de ajuste antropométrico",
            "estado": "confirmado",
            "autor": "Dr. Valenzuela",
            "fuente_ref": "FuenteDoc:acta-comite-01",
            "cuerpo": "Ajuste por IMC < 18.5 kg/m² requiere reducción del 25% en titulación basal.",
        },
        name="atom-07",
        pythonpath=pythonpath,
    )

    # SpecDoc y SpecNodeDoc: decision-renal
    diagram_dir = demo_dir / "diagrams"
    diagram_dir.mkdir(parents=True, exist_ok=True)

    node_ids = [
        "SpecNodeDoc:decision-renal.ingreso",
        "SpecNodeDoc:decision-renal.eval-crcl",
        "SpecNodeDoc:decision-renal.suspension",
        "SpecNodeDoc:decision-renal.titulacion-std",
    ]

    api.create_document(
        store_path,
        "SpecDoc",
        diagram_dir / "decision-renal.md",
        {
            "id": "decision-renal",
            "title": "Diagrama de Decisión Renal",
            "diagram_type": "activity",
            "version": "1.0",
            "spec_path": "diagrams/decision-renal.yaml",
            "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "notation": "NotationDoc:activity",
            "nodes": node_ids,
            "description": "Flujo de decisión renal para protocolo Levira.",
        },
        name="decision-renal",
        pythonpath=pythonpath,
    )

    api.create_document(
        store_path,
        "SpecNodeDoc",
        diagram_dir / "decision-renal.ingreso.md",
        {
            "id": "decision-renal.ingreso",
            "title": "Ingreso Paciente",
            "spec": "SpecDoc:decision-renal",
            "element": "ingreso",
            "kind": "initial",
            "description": "Punto de entrada de paciente a protocolo.",
        },
        name="decision-renal.ingreso",
        pythonpath=pythonpath,
    )

    api.create_document(
        store_path,
        "SpecNodeDoc",
        diagram_dir / "decision-renal.eval-crcl.md",
        {
            "id": "decision-renal.eval-crcl",
            "title": "CrCl < 30 mL/min?",
            "spec": "SpecDoc:decision-renal",
            "element": "eval-crcl",
            "kind": "decision",
            "atom_refs": ["AtomDoc:atom-04"],
            "description": "Evaluación de clearance de creatinina.",
        },
        name="decision-renal.eval-crcl",
        pythonpath=pythonpath,
    )

    api.create_document(
        store_path,
        "SpecNodeDoc",
        diagram_dir / "decision-renal.suspension.md",
        {
            "id": "decision-renal.suspension",
            "title": "Suspensión Inmediata Protocolo",
            "spec": "SpecDoc:decision-renal",
            "element": "suspension",
            "kind": "action",
            "atom_refs": ["AtomDoc:atom-04"],
            "description": "Suspensión mandatoria de protocolo clínico.",
        },
        name="decision-renal.suspension",
        pythonpath=pythonpath,
    )

    api.create_document(
        store_path,
        "SpecNodeDoc",
        diagram_dir / "decision-renal.titulacion-std.md",
        {
            "id": "decision-renal.titulacion-std",
            "title": "Titulación Basal Estándar 100%",
            "spec": "SpecDoc:decision-renal",
            "element": "titulacion-std",
            "kind": "action",
            "description": "Continuar con dosis basal nominal.",
        },
        name="decision-renal.titulacion-std",
        pythonpath=pythonpath,
    )

    # InformeDoc: doc-levira-fase2
    informe_payload = {
        "title": "Informe Clínico Levira",
        "version": "v2.4.1",
        "fuente_ref": "FuenteDoc:acta-comite-01",
        "objetivo": (
            "El presente informe consolida los criterios clínicos de dosificación y exclusión "
            "establecidos por el Comité Central para el ensayo Fase II de Levira."
        ),
        "criterios": ["AtomDoc:atom-04", "AtomDoc:atom-05"],
        "decision_spec": "SpecDoc:decision-renal",
        "tabla_dosis": [
            {
                "cohorte": "Fase II - A",
                "imc": "< 18.5",
                "ajuste": "-25% titulación",
                "origen_ref": "AtomDoc:atom-07#cuerpo",
            },
            {
                "cohorte": "Fase II - B",
                "imc": "18.5 - 24.9",
                "ajuste": "100% dosis nominal",
                "origen_ref": "protocolo-std",
            },
            {
                "cohorte": "Fase II - C",
                "imc": "≥ 25.0",
                "ajuste": "Ajuste por sup. corporal",
                "origen_ref": "norma-renal-03",
            },
        ],
        "tolerancia": (
            "Las pruebas cruzadas de interacción se mantienen bajo bandera de observación preliminar "
            "hasta recibir el panel de metabolitos plasmáticos. Los datos de telemetría se reportan con frecuencia cuatrisemanal."
        ),
    }

    api.create_document(
        store_path,
        "InformeDoc",
        demo_dir / "informe-clinico.md",
        informe_payload,
        name="doc-levira-fase2",
        pythonpath=pythonpath,
    )

    # Reindexar relaciones
    print("[*] Reconstruyendo índice de aristas...")
    api.load_edge_index(store_path)

    # 5. Verificación de segmentos y resolución
    print("[*] Verificando /document/segments...")
    segments = build_document_segments(store_path, pythonpath, "InformeDoc/doc-levira-fase2")
    print(f"    Texto renderizado: {len(segments.text)} caracteres")
    print(f"    Segmentos generados: {len(segments.segments)}")

    # Comprobar enriquecimiento de diagrama
    found_diagram = False
    for s in segments.segments:
        if getattr(s, "field", None) == "decision_spec" or "diagram" in getattr(s, "traits", []):
            found_diagram = True
            proj = getattr(s, "projection", None)
            print(f"    [+] Segmento de diagrama detectado: projection={bool(proj)}")
            if proj and "nodes" in proj:
                print(f"        Nodos resueltos en proyección: {len(proj['nodes'])}")

    print("\n[OK] Store de prueba configurado con éxito en: " + str(demo_dir))
    return demo_dir


if __name__ == "__main__":
    main()
