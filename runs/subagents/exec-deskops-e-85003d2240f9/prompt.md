Task: task-la-puerta-identidad-de-tools-check-sh-clasifica-workbench-demo-store-demo-del-workbench-de-surface-e
Title: La puerta identidad de tools/check.sh clasifica workbench_demo (store demo del workbench de surface) en contracts/identity.toml
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: closed [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .
  blocked by: error: [rules/rule-activation-task-code] TaskCodeDoc:task-la-puerta-identidad-de-tools-check-sh-clasifica-workbench-demo-store-demo-del-workbench-de-surface-e: Una tarea task.code se activa con recibos preflight y bundle aceptados e intactos y sus dependencias cerradas. | any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "bundle") (seen: {}) (witness: ReviewDoc:review-task-la-puerta-identidad-de-tools-check-sh-clasifica-workbench-demo-store-demo-del-workbench-de-surface-e-preflight-1 {"anchor_state":"changed"})

---
sldb:
  by: agent
  at: '2026-11-25T02:32:01Z'
  authority: generated
  via: save_document_payload
id: task-la-puerta-identidad-de-tools-check-sh-clasifica-workbench-demo-store-demo-del-workbench-de-surface-e
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

# La puerta identidad de tools/check.sh clasifica workbench_demo (store demo del workbench de surface) en contracts/identity.toml

## Rationale

_Explain why this task exists or the business driver behind it._

Desde 562847e2 (asistente y tour del workbench) el repo versiona workbench_demo/ en la raiz y contracts/identity.toml no lo clasifica: bash tools/check.sh --fast termina en rc 1 por 'directorio versionado sin clasificar en la raiz: workbench_demo'. Los testers de deskops tratan rc distinto de 0 como FALLA, asi que la puerta falla en todas las tareas de sldb (lector de surface, attach_atom_edges, plan Datalog del 2026-11-23) aunque el cambio no lo toque.

## Goal

_Describe the concrete result this task must produce._

contracts/identity.toml clasifica workbench_demo/ como [[foreign]] (decision tomada: datos de demo de surface), con what y verdict que dicen por que existe; bash tools/check.sh --fast sale con rc 0. files se recalcula con git ls-files al ejecutar.

## Scope

_State what is in scope and what is out of scope._

Solo contracts/identity.toml (un bloque [[foreign]]). No tocar tools/check_identity.py ni su test, ni mover o borrar workbench_demo/. Validacion en el arbol de trabajo de la tarea.

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo: /mnt/ssd/proyectos/SLDB_1/sldb, en el arbol de trabajo de la tarea (no hace falta estar en main). Decision tomada (coordinador, 2026-11-24): workbench_demo/ es ajeno, igual que surface/: un store de demo que usa el tour del workbench de surface, no producto ni autoaplicacion. Cambio unico: agregar en contracts/identity.toml, junto a los [[foreign]] existentes de 'surface' y 'sldb' (mismas cuatro claves), un bloque [[foreign]] con path = "workbench_demo", files = <salida de 'git ls-files workbench_demo | wc -l', hoy 213>, what = "store de demo del workbench de surface (asistente y tour, 562847e2)" y verdict = "datos de demo de surface, no producto ni autoaplicacion; lo usa el tour del workbench". La nota de por que existe es esa clave what/verdict, no un comentario aparte. No tocar tools/check_identity.py salvo que check.sh siga en rojo por la puerta identidad despues del bloque; en ese caso parar y reportar en vez de cambiar la puerta. No mover ni borrar workbench_demo/.

## Validation

_List the checks required before this task can close._

- bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

contracts/identity.toml tiene el bloque [[foreign]] de workbench_demo con path, files, what y verdict, y bash tools/check.sh --fast sale con rc 0 (la puerta identidad sin violaciones).

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-la-puerta-identidad-de-tools-check-sh-clasifica-workbench-demo-store-demo-del-workbench-de-surface-e"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-85003d2240f9"

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-85003d2240f9`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-85003d2240f9

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
