---
sldb:
  by: agent
  at: '2026-11-16T07:41:04Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-dónde-se-agrupan-los-ausentes-de-sections-rebuild
status: active
summary: dónde se agrupan los ausentes de Sections rebuild
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: dónde se agrupan los ausentes de Sections rebuild

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

src/sldb/store/section_sync.py, src/sldb/store/semantic.py

## How

_Describe the correct way to apply this guidance._

RebuildReport vive en src/sldb/store/semantic.py y se puede editar para agregar missing_paths: list[str]. El modelo es m_entry.name. El aviso se emite una vez por llamada a la función de section_sync que recorre los modelos; si esa función se llama por modelo, sale una línea por modelo con ausentes, y eso es válido. report.verbose sigue acumulando una entrada por ausente (no es log). Los documentos se trackean con sldb.api.create_document y después se borran sus archivos.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.
