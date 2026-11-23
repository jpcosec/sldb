---
sldb:
  by: agent
  at: '2026-11-23T17:54:19Z'
  authority: generated
  via: save_document_payload
id: task-sldb-serve-manda-composition-de-cada-field-y-expone-por-modelo-la-ruta-y-la-cardinalidad-create-resp
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261121-210430-unclear-la-superficie-trata-todo-field-como-bloque-porque-el-servidor-manda-composition-null.md
- desk/inbox/20261121-213216-unclear-la-superficie-no-puede-saber-la-ruta-ni-la-cardinalidad-de-un-modelo-al-crear-un-documento.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb serve manda composition de cada field y expone por modelo la ruta y la cardinalidad; create respeta path

## Rationale

_Explain why this task exists or the business driver behind it._

Notas 20261121-210430-unclear-la-superficie-trata-todo-field-como-bloque-porque-el-servidor-manda-composition-null y 20261121-213216-unclear-la-superficie-no-puede-saber-la-ruta-ni-la-cardinalidad-de-un-modelo-al-crear-un-documento (sesion de minegocio, 21-nov): GET /document/segments entrega cada field con composition, projection y table_data en null, y la superficie trata todo field como bloque (src/core/layout.ts:38, src/react/DocumentSurface.tsx:74, src/views/ComposerView.tsx:22), dejando las filas del frontmatter sin piezas; y la superficie no puede saber ni decidir la ruta ni la cardinalidad de un modelo al crear (POST /save action create ignora path; ningun endpoint expone patron de ruta ni cardinalidad por modelo).

## Goal

_Describe the concrete result this task must produce._

GET /document/segments distingue fields inline de bloques (composition presente solo en bloques, o un campo explicito); un endpoint de serve expone por modelo el patron de ruta y la cardinalidad declarados en el modelo; POST /save action create acepta path; la superficie usa ese dato y deja de tratar todo field como bloque.

## Scope

_State what is in scope and what is out of scope._

src/sldb/cli/serve/ (segments, save, endpoint de modelos), la declaracion de ruta y cardinalidad en el modelo si no existe (atributo de clase documentado), y en surface solo el criterio de bloque en core/layout.ts, react/DocumentSurface.tsx y views/ComposerView.tsx, con tests. Coordinar con task-surface-trae-el-lector-de-documentos-de-minegocio-...: si el lector ya porto esos archivos, este cambio va sobre la version portada. No tocar WorkbenchShell.tsx, vite.config.ts ni tsconfig.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test de serve con un documento de frontmatter tipado: los fields inline no traen composition. 2) Arreglo en segments. 3) Atributo de modelo para patron de ruta y cardinalidad, endpoint que lo expone y create que respeta path. 4) Ajuste del criterio de bloque en surface con fixture que trae fields inline.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/ -k serve; cd surface && npx tsc --noEmit && npx vitest run

## Done When

_Name the observable condition that makes the task complete._

Tests de serve y de surface (vitest) nuevos pasan; tsc y check-layers de surface pasan.
