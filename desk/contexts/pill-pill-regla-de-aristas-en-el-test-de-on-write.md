---
sldb:
  by: agent
  at: '2026-11-16T07:53:14Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-regla-de-aristas-en-el-test-de-on-write
status: active
summary: regla de aristas en el test de on_write
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: regla de aristas en el test de on_write

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

docs/architecture/rules-language.md, tests/api/test_on_write_entering.py

## How

_Describe the correct way to apply this guidance._

El lenguaje no tiene exists(); la condición del test es count(<campo de referencia>: title != "") > 0 (si ese predicado no parsea, cualquier predicado sobre un campo del documento destino que los tests de tests/api/test_rules.py ya usen), con la forma count(camino: p) cmp término de docs/architecture/rules-language.md (líneas 36 y 127-135), sobre un campo declarado en __references__ del modelo de prueba. Las aristas salientes que el payload nuevo ya no declara se quitan del grafo de evaluación. DocumentReference (src/sldb/api/documents/document_reference.py) es pydantic: alerts: list[dict[str, Any]] = Field(default_factory=list). Para aislar listeners se usa monkeypatch.setattr sobre sldb.core.finding_route._LISTENERS (lista vacía). tests/api/test_rules_evaluation.py es solo regresión.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.
