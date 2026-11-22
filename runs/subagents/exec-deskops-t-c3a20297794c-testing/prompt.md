Task: task-heading-scan-scan-heading-bodies-baja-a-10-lineas-de-logica-regla-de-codigo-limpio
Title: heading_scan: scan_heading_bodies baja a 10 líneas de lógica (regla de código limpio)
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
  at: '2026-11-22T12:53:43Z'
  authority: generated
  via: save_document_payload
id: task-heading-scan-scan-heading-bodies-baja-a-10-lineas-de-logica-regla-de-codigo-limpio
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

# heading_scan: scan_heading_bodies baja a 10 líneas de lógica (regla de código limpio)

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-22: la tarea del guard de sobrescritura con pérdida agotó sus intentos de tester. El reap perdió el commit del intento 2 y el coordinador lo recuperó y trajo a main como 074bc3bc. Funciona: tests/api/test_lossy_overwrite_content.py da 6 passed y tests/api 649 passed (verificación en runs/subagents/20261122-verif-guard-lossy/verificacion.log). Pero tests/test_clean_code_rules.py falla: 'Function scan_heading_bodies in heading_scan.py has 11 lines of logic (max 10)'. Bloquea el integrate de sldb.

## Goal

_Describe the concrete result this task must produce._

src/sldb/api/documents/heading_scan.py cumple tests/test_clean_code_rules.py: scan_heading_bodies queda en 10 líneas de lógica o menos, partiéndola en una auxiliar privada del mismo archivo, sin cambiar el comportamiento.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/api/documents/heading_scan.py. Fuera: cambiar tests o comportamiento.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: partir scan_heading_bodies. p2: correr tests/test_clean_code_rules.py, tests/api/test_lossy_overwrite_content.py y tests/test_extraction_segments.py, en verde. p3: bash tools/check.sh --fast en verde salvo 'identidad' por workbench_demo (excepción f055723d). p4: commit desde el worktree que dispatch te da con 'git commit -- src/sldb/api/documents/heading_scan.py' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo. Las métricas son las del test: líneas de lógica = del primer al último statement del cuerpo, sin docstring.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_clean_code_rules.py tests/api/test_lossy_overwrite_content.py

## Done When

_Name the observable condition that makes the task complete._

Los tres archivos de tests pasan.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-heading-scan-scan-heading-bodies-baja-a-10-lineas-de-logica-regla-de-codigo-limpio"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
