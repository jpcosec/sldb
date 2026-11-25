Task: task-el-422-de-post-save-de-sldb-serve-devuelve-exc-errors-como-details
Title: El 422 de POST /save de sldb serve devuelve exc.errors() como details
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-25T03:47:53Z'
  authority: generated
  via: save_document_payload
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

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-el-422-de-post-save-de-sldb-serve-devuelve-exc-errors-como-details"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-891c1b240153"

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-891c1b240153`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-891c1b240153

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
