---
sldb:
  by: agent
  at: '2026-11-16T07:55:57Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-standards-md-es-un-documento-modelado
status: active
summary: STANDARDS.md es un documento modelado
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: STANDARDS.md es un documento modelado

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

desk/STANDARDS.md, docs/architecture/store-extraction-proposal.md

## How

_Describe the correct way to apply this guidance._

desk/STANDARDS.md está trackeado en el store de sldb y su regla 4 dice que se edita con sldb fields update, no a mano. La línea de la decisión 6 se cambia con sldb fields update sobre el campo que la contiene. Si JP elige (a), la tarea de refactor no inyecta costuras nuevas (el desacople ya está, beb8a99c): crea el paquete y mueve el store detrás de las costuras existentes. La sección del doc se titula exactamente '## Decisión 6'.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.
