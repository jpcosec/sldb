---
sldb:
  by: agent
  at: '2026-11-16T07:54:56Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-alcance-real-del-traslado-del-parser-a-core
status: active
summary: alcance real del traslado del parser a core
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: alcance real del traslado del parser a core

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

src/sldb/store/graph/language/predicate_parser.py, src/sldb/store/graph/language/predicate_tokens.py, src/sldb/store/graph/language/predicate_cursor.py, src/sldb/store/exceptions.py

## How

_Describe the correct way to apply this guidance._

El parser importa también predicate_atoms, y este a predicate_paths y predicate_terms; predicate_paths importa predicate_reach: esos cuatro módulos se mueven junto con los cuatro si no importan nada de sldb.store fuera del paquete language. predicate_tokens importa unquote de sldb.store.query_engine.where_literal, y predicate_cursor y predicate_tokens importan WherePredicateError de sldb.store.exceptions. WherePredicateError ya existe en sldb.core.exceptions, así que se importa de ahí. unquote se mueve a core si es una función pura de texto, y where_literal la reimporta. Si aparece cualquier otra dependencia de store, la tarea se detiene. Cada shim es un módulo con 'from sldb.core.rules_language.<mod> import *' y el mismo __all__.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.
