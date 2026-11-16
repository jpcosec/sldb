---
sldb:
  by: agent
  at: '2026-11-16T07:39:03Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-campo-data-de-specdoc
status: active
summary: campo data de SpecDoc
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: campo data de SpecDoc

## What

_Define the context or guardrail this pill carries._

Las respuestas del bundle-1 de la tarea: precisiones de implementación que la revisión en frío pidió y que el contrato deja abiertas.

## Why

_Explain why this context matters for safe execution._

La revisión cold-bundle (bundle-1) mostró que sin estas precisiones el ejecutor tendría que inventar estos detalles.

## When

_Describe when an agent should apply this pill._

Al ejecutar la tarea, antes de tocar código.

## Where

_Name the files, surfaces, or scope this pill applies to._

src/sldb/models/notation/spec_doc.py, src/sldb/models/notation/view_section.py, src/sldb/api/notations/spec_sync_docs.py

## How

_Describe the correct way to apply this guidance._

style ya es un escalar en la raíz del spec y queda fuera de data. Elementos son las claves de data que spec_sync_docs.py ya mapea a nodos o aristas para cada tipo de diagrama (leer qué claves toma en cada caso); el resto va a data. Para serializar el dict se usa la misma técnica que el campo select de ViewSection (view_section.py, un dict con su validador _select); si su marcador no sirve para un dict libre, data se guarda como texto YAML en un campo de bloque y un validador lo convierte en dict. El test de style compara el valor style del resultado de resolve_view con el del SpecDoc, sea cual sea la forma de ese resultado.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.
