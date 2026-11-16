---
sldb:
  by: agent
  at: '2026-11-16T07:43:25Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-forma-del-rechazo-de-dominio-en-sldb-mcp
status: active
summary: forma del rechazo de dominio en sldb mcp
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: forma del rechazo de dominio en sldb mcp

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

src/sldb/mcp/write/apply.py, src/sldb/mcp/write/tools.py

## How

_Describe the correct way to apply this guidance._

apply.rejected(cause, explanation, **detail) devuelve un dict con detail expandido, así que findings=lista queda como clave 'findings'. propose_changes y apply_changes responden los dos con ese mismo dict cuando hay errores de dominio. 'domain_alerts' se agrega al dict del dry-run de propose y al resultado de apply. Los validadores reciben los mismos objetos de cambio que tiene cada método (Change en propose, BatchChange en apply) y la firma se documenta como 'list de cambios del lote'. Los tres casos nuevos van en tests/mcp/test_extension.py; tests/mcp/test_write_tools.py se corre como regresión.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.
