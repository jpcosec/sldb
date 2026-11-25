FILE:desk/tasks/task-el-422-de-post-save-de-sldb-serve-devuelve-exc-errors-como-details.md
---
sldb:
  by: agent
  at: '2026-11-25T01:16:03Z'
  authority: generated
  via: create_document
id: task-el-422-de-post-save-de-sldb-serve-devuelve-exc-errors-como-details
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

# El 422 de POST /save de sldb serve devuelve exc.errors() como details

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de minegocio (sldb 61c5847f). Partida en 4 tareas chicas al replanificar en DAG (JP 2026-11-24).

## Goal

_Describe the concrete result this task must produce._

Cuando POST /save rechaza un documento por validacion, la respuesta 422 trae details con exc.errors() de pydantic.

## Scope

_State what is in scope and what is out of scope._

La ruta save de src/sldb/cli/serve/ y un test. Fuera: lo demas de serve.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test: save con un campo invalido devuelve 422 con details de pydantic. 2) Arreglo. Correr solo el test.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_serve_save_422.py

## Done When

_Name the observable condition that makes the task complete._

El test del 422 con details pasa.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-el-422-de-post-save-de-sldb-serve-devuelve-exc-errors-como-details: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

