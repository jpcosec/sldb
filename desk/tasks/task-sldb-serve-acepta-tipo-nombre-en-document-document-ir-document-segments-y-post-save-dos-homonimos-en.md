---
sldb:
  by: agent
  at: '2026-11-25T01:15:26Z'
  authority: generated
  via: create_document
id: task-sldb-serve-acepta-tipo-nombre-en-document-document-ir-document-segments-y-post-save-dos-homonimos-en
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb serve acepta Tipo/nombre en /document, /document/ir, /document/segments y POST /save (dos homonimos en modelos distintos)

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de minegocio (sldb 61c5847f). Partida en 4 tareas chicas al replanificar en DAG (JP 2026-11-24).

## Goal

_Describe the concrete result this task must produce._

Las rutas de documento de sldb serve aceptan un selector Tipo/nombre ademas del nombre, y dos documentos con el mismo nombre en modelos distintos se abren y se guardan cada uno.

## Scope

_State what is in scope and what is out of scope._

Resolucion del selector en src/sldb/cli/serve/ y un test. Guia: la prueba xfail test_dos_paginas_con_el_mismo_nombre_se_abren_y_se_guardan_cada_una de minegocio. Fuera: cache, lectura tolerante, 422.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test con dos homonimos en modelos distintos por las cuatro rutas. 2) Resolver Tipo/nombre. Correr solo el test nuevo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_serve_tipo_nombre.py

## Done When

_Name the observable condition that makes the task complete._

El test de homonimos pasa por las cuatro rutas.
