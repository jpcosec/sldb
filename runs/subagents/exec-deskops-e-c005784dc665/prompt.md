Task: task-sldb-docs-create-o-resuelve-la-ruta-contra-el-cwd-o-avisa
Title: sldb docs create -o resuelve la ruta contra el cwd (o avisa)
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
  at: '2026-11-25T03:49:55Z'
  authority: generated
  via: save_document_payload
id: task-sldb-docs-create-o-resuelve-la-ruta-contra-el-cwd-o-avisa
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

# sldb docs create -o resuelve la ruta contra el cwd (o avisa)

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de minegocio (sldb 61c5847f). Partida en 3 tareas chicas al replanificar en DAG (JP 2026-11-24).

## Goal

_Describe the concrete result this task must produce._

Contrato elegido: sldb docs create -o <ruta relativa> resuelve la ruta contra el directorio actual del proceso (no contra la raiz del store) y escribe ahi.

## Scope

_State what is in scope and what is out of scope._

El comando docs create y un test. Fuera: render y fields.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Encontrar docs create en src/sldb/cli/ (grep -rn 'def.*create' src/sldb/cli/ | grep -i doc). 2) Test NUEVO tests/test_docs_create_output_path.py: store temporal, cwd = un subdirectorio del proyecto, docs create -o sub.md -> el archivo queda en <cwd>/sub.md. 3) Arreglo. Correr solo ese test.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_docs_create_output_path.py

## Done When

_Name the observable condition that makes the task complete._

El test de docs create -o relativa pasa.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-sldb-docs-create-o-resuelve-la-ruta-contra-el-cwd-o-avisa"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-c005784dc665"

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-c005784dc665`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-c005784dc665

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
