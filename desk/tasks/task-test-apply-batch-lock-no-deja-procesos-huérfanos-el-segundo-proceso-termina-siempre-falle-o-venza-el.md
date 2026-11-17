---
sldb:
  by: agent
  at: '2026-11-17T12:35:02Z'
  authority: generated
  via: create_document
id: task-test-apply-batch-lock-no-deja-procesos-huérfanos-el-segundo-proceso-termina-siempre-falle-o-venza-el
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261117-092921-suggestion-procesos-hu-rfanos-de-test-second-process-with-the-s-apply-batch-con-hold-en-dev-shm.md
depends_on: []
pills: []
files:
- tests/api/test_apply_batch_lock.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-apply-batch-prevalida-y-escribe-bajo-el-cerrojo-del-store-y-rechaza-con-conflicterror-un-guarda-obso
---

# test_apply_batch_lock no deja procesos huérfanos: el segundo proceso termina siempre, falle o venza el test

## Rationale

_Explain why this task exists or the business driver behind it._

En robocop2 quedaron dos procesos huérfanos de tests/api/test_apply_batch_lock.py (test_second_process_with_the_same_guard_conflicts_and_leaves_no_partial_write), uno de 19 h y otro de 16 h, esperando un archivo marks/go que nunca llega: la prueba no limpia el proceso que retiene el cerrojo si falla o vence su timeout. Ocupan memoria en una máquina que ya colapsó por RAM. Origen: desk/inbox/20261117-092921-suggestion-procesos-hu-rfanos-de-test-second-process-with-the-s-apply-batch-con-hold-en-dev-shm.md.

## Goal

_Describe the concrete result this task must produce._

Cada proceso que lanza test_apply_batch_lock.py termina siempre al salir del test (pase, falle o venza), y la espera del archivo de señal tiene un tope; un test que falla no deja ningún proceso vivo.

## Scope

_State what is in scope and what is out of scope._

Entra: en tests/api/test_apply_batch_lock.py, lanzar los procesos en un contexto que los mata y los espera en finally (o una fixture con yield), y poner un tope de tiempo a la espera de marks/go dentro del proceso hijo, para que salga solo si el padre muere; un test que simula un fallo del padre y comprueba que no queda ningún hijo vivo. No entra: cambiar apply_batch ni lock.py.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer tests/api/test_apply_batch_lock.py. 2) Implementar la limpieza y el tope. 3) Test del caso de fallo. 4) Validation, comprobando con ps que no quedan procesos del test.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_apply_batch_lock.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; tras forzar un fallo del test no queda ningún proceso python del test vivo; commit; aviso a IR.
