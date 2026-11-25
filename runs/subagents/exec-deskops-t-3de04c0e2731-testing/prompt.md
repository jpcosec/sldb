Task: task-el-422-de-post-save-de-sldb-serve-devuelve-exc-errors-como-details
Title: El 422 de POST /save de sldb serve devuelve exc.errors() como details
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

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

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-el-422-de-post-save-de-sldb-serve-devuelve-exc-errors-como-details"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-3de04c0e2731"

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
