---
sldb:
  by: agent
  at: '2026-11-16T07:45:27Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-texto-de-la-alerta-y-test-existente-de-stale
status: active
summary: texto de la alerta y test existente de stale
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: texto de la alerta y test existente de stale

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

src/sldb/cli/commands/edges.py, tests/api/test_api_edges.py

## How

_Describe the correct way to apply this guidance._

El texto de la alerta cubre todas las causas de stale: 'shard out of date (missing, built by another version, or the file changed outside sldb)', con fix 'sldb stores update'. El test se hace extendiendo el que ya existe (test_a_hand_edit_reaches_the_index_through_stores_update): antes de stores update se afirma que el documento está en stale y que rebuild_edges no lo saca. Del grep solo se cambian los textos que mandan a 'edges rebuild' para resolver stale.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.
