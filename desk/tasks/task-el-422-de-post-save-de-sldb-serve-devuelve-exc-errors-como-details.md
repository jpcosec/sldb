---
sldb:
  by: agent
  at: '2026-11-25T05:32:06Z'
  authority: generated
  via: save_document_payload
id: task-el-422-de-post-save-de-sldb-serve-devuelve-exc-errors-como-details
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
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

Cuando POST /save de sldb serve rechaza un documento por validacion de pydantic, responde 422 con un JSON cuya clave 'details' es exactamente la lista exc.errors() (serializable: loc, msg, type), ademas de lo que ya devuelve.

## Scope

_State what is in scope and what is out of scope._

La ruta save de src/sldb/cli/serve/ y un test. Fuera: lo demas de serve.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Encontrar el manejador de POST /save en src/sldb/cli/serve/ (grep -rn 'save' src/sldb/cli/serve/) y donde captura ValidationError. 2) Test NUEVO tests/test_serve_save_422.py siguiendo cualquier test existente de serve (grep -ln 'serve' tests/): un modelo minimo con un campo int, save con ese campo en 'abc' -> status 422 y body['details'] es una lista no vacia con loc que nombra el campo. 3) Arreglo. Correr solo ese test.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_serve_save_422.py

## Done When

_Name the observable condition that makes the task complete._

El test del 422 con details pasa.
