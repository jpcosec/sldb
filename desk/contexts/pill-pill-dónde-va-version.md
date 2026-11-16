---
sldb:
  by: agent
  at: '2026-11-16T07:44:26Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-dónde-va-version
status: active
summary: dónde va --version
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: dónde va --version

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

src/sldb/cli/parsers/core.py, src/sldb/store/package_version.py

## How

_Describe the correct way to apply this guidance._

El parser raíz se construye en src/sldb/cli/parsers/core.py (build_parser) y ahí va --version. Se agrega una función nueva _source_checkout_dir() que hace el mismo recorrido y devuelve el directorio del pyproject, sin cambiar _source_checkout_version. En el test se parchea source_revision para devolver 'v0.1.13-1-gabc' y se comprueba que la salida contiene '(v0.1.13-1-gabc at '. La versión sale de package_version().

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.
