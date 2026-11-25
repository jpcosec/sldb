---
sldb:
  by: agent
  at: '2026-11-25T01:18:40Z'
  authority: generated
  via: save_document_payload
id: task-sldb-serve-manda-composition-de-cada-field-y-expone-por-modelo-la-ruta-y-la-cardinalidad-create-resp
status: draft
summary: ''
tags: []
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

GET /document/segments distingue fields inline de bloques: composition viene solo en bloques (o un campo explicito lo dice).

## Scope

_State what is in scope and what is out of scope._

segments en src/sldb/cli/serve/ y un test. Fuera: ruta y cardinalidad del modelo, create con path, surface.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test con un documento de frontmatter tipado: los fields inline no traen composition, los bloques si. 2) Arreglo en segments. Correr solo el test.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_serve_segments_composition.py

## Done When

_Name the observable condition that makes the task complete._

El test de segments pasa: inline sin composition, bloques con composition.
