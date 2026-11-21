Task: task-notations-validate-check-store-document-baja-a-10-lineas-de-logica-regla-de-codigo-limpio
Title: notations validate: _check_store_document baja a 10 líneas de lógica (regla de código limpio)
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
  at: '2026-11-21T03:13:45Z'
  authority: generated
  via: save_document_payload
id: task-notations-validate-check-store-document-baja-a-10-lineas-de-logica-regla-de-codigo-limpio
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
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

# notations validate: _check_store_document baja a 10 líneas de lógica (regla de código limpio)

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21: la tarea de sldb notations validate agotó sus intentos. Su intento 2 (5c1740d2, ya en main) funciona (tests/notations/test_notations_validate_cli.py 11 passed, test_notations_sync_spec_cli.py 4 passed, selfdoc check en 0; verificación del coordinador en runs/subagents/20261121-verif-notations-validate/verificacion.log), pero tests/test_clean_code_rules.py falla: 'Function _check_store_document in notations_validate.py has 14 lines of logic (max 10)'. Bloquea el integrate de sldb, y con él el retiro de spec2viz (IR13).

## Goal

_Describe the concrete result this task must produce._

src/sldb/cli/commands/notations_validate.py cumple tests/test_clean_code_rules.py: _check_store_document queda en 10 líneas de lógica o menos, partiéndola en funciones auxiliares privadas en el mismo archivo (o en un módulo hermano si el archivo pasa de 80 líneas efectivas), sin cambiar el comportamiento.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/cli/commands/notations_validate.py y, si hace falta, un módulo hermano en la misma carpeta. Fuera: cambiar comportamiento, tests o límites.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: partir _check_store_document en auxiliares privadas. p2: correr tests/test_clean_code_rules.py, tests/notations/test_notations_validate_cli.py y tests/notations/test_notations_sync_spec_cli.py, de a uno, en verde. p3: bash tools/check.sh --fast en verde salvo 'identidad' por workbench_demo (excepción autorizada). p4: commit desde tu worktree con 'git commit -- <rutas>' y trailer Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_clean_code_rules.py tests/notations/test_notations_validate_cli.py

## Done When

_Name the observable condition that makes the task complete._

Los tres archivos de tests pasan.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-notations-validate-check-store-document-baja-a-10-lineas-de-logica-regla-de-codigo-limpio"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
