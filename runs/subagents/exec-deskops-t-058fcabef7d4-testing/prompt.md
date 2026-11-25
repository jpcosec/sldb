Task: task-la-puerta-identidad-de-tools-check-sh-clasifica-workbench-demo-store-demo-del-workbench-de-surface-e
Title: La puerta identidad de tools/check.sh clasifica workbench_demo (store demo del workbench de surface) en contracts/identity.toml
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
  at: '2026-11-25T03:13:54Z'
  authority: generated
  via: save_document_payload
id: task-la-puerta-identidad-de-tools-check-sh-clasifica-workbench-demo-store-demo-del-workbench-de-surface-e
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

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-la-puerta-identidad-de-tools-check-sh-clasifica-workbench-demo-store-demo-del-workbench-de-surface-e"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-058fcabef7d4"

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
