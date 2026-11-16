---
sldb:
  by: agent
  at: '2026-11-16T07:42:25Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-rechazados-de-la-carga-tolerante
status: active
summary: rechazados de la carga tolerante
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: rechazados de la carga tolerante

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

src/sldb/store/query.py, src/sldb/api/documents/runtime_documents.py

## How

_Describe the correct way to apply this guidance._

src/sldb/store/query.py se puede editar: _load_accepted recibe una lista opcional rejected y le agrega (ruta, modelo, mensaje) cuando el modelo rechaza un documento; los llamadores actuales no pasan la lista y no cambian. Solo se envuelve en SLDBValidationError una excepción que no lo sea ya, con 'raise ... from exc'. stores build --check no es requisito de cierre.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.
