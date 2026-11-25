---
sldb:
  by: agent
  at: '2026-11-25T01:19:44Z'
  authority: generated
  via: create_document
id: task-surface-deja-de-tratar-todo-field-como-bloque-usa-composition-de-segments-y-la-ruta-y-cardinalidad-d
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on:
- task-sldb-serve-manda-composition-de-cada-field-y-expone-por-modelo-la-ruta-y-la-cardinalidad-create-resp
- task-los-modelos-de-sldb-declaran-patron-de-ruta-y-cardinalidad-serve-los-expone-por-modelo-y-post-save-c
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# surface deja de tratar todo field como bloque: usa composition de segments y la ruta y cardinalidad del modelo

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de minegocio (sldb 61c5847f). Partida en 3 tareas chicas al replanificar en DAG (JP 2026-11-24).

## Goal

_Describe the concrete result this task must produce._

surface/src/core/layout.ts, react/DocumentSurface.tsx y views/ComposerView.tsx usan composition de /document/segments para decidir bloque o inline, y la ruta y cardinalidad del endpoint de modelos al crear.

## Scope

_State what is in scope and what is out of scope._

Esos tres archivos de surface y sus tests, con una fixture con fields inline. No tocar WorkbenchShell.tsx, vite.config.ts ni tsconfig.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Fixture con fields inline. 2) Criterio de bloque por composition. 3) Crear con la ruta del modelo. 4) tsc y vitest de los archivos tocados.

## Validation

_List the checks required before this task can close._

- cd surface && npx tsc --noEmit && npx vitest run src/core src/react src/views

## Done When

_Name the observable condition that makes the task complete._

Con la fixture, los fields inline se muestran inline; tsc y los tests tocados pasan.
