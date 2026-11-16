---
sldb:
  by: agent
  at: '2026-11-16T07:37:41Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-salida-y-orden-de-sldb-notations-validate
status: active
summary: salida y orden de sldb notations validate
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: salida y orden de sldb notations validate

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

src/sldb/cli/parsers/notations.py, src/sldb/cli/commands/notations.py

## How

_Describe the correct way to apply this guidance._

La salida usa el mismo flag que sync (--json); no se inventa --format. Las alertas no cambian el exit code: 0 sin errores, 1 con algún error, 2 si el objetivo es desconocido. Orden de intentos para un archivo: paleta (clave palette o colors en la raíz), spec (clave type, y los tipos válidos son los que acepta load_spec, sin enumerarlos aquí) y notación (load_notation). Sin --store se usan solo las builtin.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.
