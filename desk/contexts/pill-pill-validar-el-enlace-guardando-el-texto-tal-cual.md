---
sldb:
  by: agent
  at: '2026-11-16T07:48:29Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-validar-el-enlace-guardando-el-texto-tal-cual
status: active
summary: validar el enlace guardando el texto tal cual
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: validar el enlace guardando el texto tal cual

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

src/sldb/api/stores/link_store.py, src/sldb/cli/commands/store_add.py

## How

_Describe the correct way to apply this guidance._

raw se agrega a link_store (src/sldb/api/stores/link_store.py:19), que lo pasa a record_store_link. Para validar (_check_other_exists, resolve), se usa el texto expandido con os.path.expandvars(os.path.expanduser(raw)); lo que se guarda es raw sin expandir. La expansión al leer se hace solo en _linked_stores, no en _resolve_path general. El comando es src/sldb/cli/commands/store_add.py.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.
