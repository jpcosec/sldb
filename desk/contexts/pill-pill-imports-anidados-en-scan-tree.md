---
sldb:
  by: agent
  at: '2026-11-16T07:36:00Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-imports-anidados-en-scan-tree
status: active
summary: imports anidados en scan_tree
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: imports anidados en scan_tree

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

src/sldb/code/imports.py, src/sldb/code/scan.py, src/sldb/api/notations/component_spec_python.py

## How

_Describe the correct way to apply this guidance._

py_nested_imports(root, src) recibe los mismos argumentos que py_imports(root, src) (src son los bytes del fuente) y devuelve las cadenas con el mismo formato que py_imports, una por sentencia. attrs['nested_imports'] guarda esa lista con el mismo formato que attrs['imports']. La deduplicación contra las de nivel superior se hace en component_spec_python después de resolver los imports relativos, sobre el par (módulo fuente, módulo destino) ya resuelto.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.
