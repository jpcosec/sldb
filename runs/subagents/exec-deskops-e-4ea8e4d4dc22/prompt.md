Task: task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes
Title: Regresión: persistir el conjunto de documentos sucios (6772820a) rompe 16 tests de transacciones en tests/api
Status: draft
Current node: ritual-execution
Task type: task.debug
Lifecycle gates:
- task_activates -> ritual-testing: closed [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .
  blocked by: error: [rules/rule-activation-task-debug] TaskDebugDoc:task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes: Una tarea task.debug se activa con recibos preflight y reproduction aceptados e intactos y sus dependencias cerradas. | any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "reproduction") (seen: {}) (witness: ReviewDoc:review-task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes-bundle-1 {"kind":"bundle"})

---
sldb:
  by: agent
  at: '2026-11-21T12:47:13Z'
  authority: generated
  via: create_document
id: task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Regresión: persistir el conjunto de documentos sucios (6772820a) rompe 16 tests de transacciones en tests/api

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21: 6772820a ('Persist the dirty document set in .sldb_cache so incremental mode works across processes', tarea el-conjunto-de-documentos-sucios, closeout local 1e0d219c, NO integrado) rompe tests/api. Reproducción en worktree limpio: python -m pytest -q -p no:cacheprovider -n 4 tests/api/test_transaction_rules_dirty.py tests/api/test_transaction.py tests/api/test_write_paths_validate.py da 25 passed sobre 6772820a~1 y 9 failed sobre 6772820a. tests/api completo da 16 failed sobre main local y 643 passed sobre origin/main. Fallan, entre otros, test_an_absent_dirty_set_stays_absent_after_a_failed_transaction, test_a_stale_source_hash_after_a_write_is_a_conflict_not_a_rollback_error, test_a_failure_during_the_rollback_is_raised_with_the_unrestored_paths y test_transaction_rejects_what_the_model_rejects_and_rolls_back: el rollback de una transacción no restaura o no tiene en cuenta el conjunto sucio persistido. El tester de esa tarea dio FALLA solo por 'identidad' sin correr tests/api; el coordinador la cerró sin verlo.

## Goal

_Describe the concrete result this task must produce._

tests/api vuelve a verde completo con el conjunto sucio persistido: una transacción fallida deja el conjunto persistido (en .sldb_cache) igual que antes de empezar, incluido el caso en que no existía; un hash de origen viejo sigue siendo conflicto y no error de rollback; un fallo durante el rollback sigue informando las rutas no restauradas. Se mantiene el objetivo de 6772820a (el modo incremental funciona entre procesos, tests/store/test_merkle_operation_cache.py en verde). No se cambian los asserts de los tests de tests/api.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/store/documents_dirty.py, documents_dirty_persist.py, el código de transacciones/rollback de sldb que maneje el conjunto sucio, y un test nuevo si hace falta. Fuera: cambiar los tests existentes de tests/api.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: reproducir con el comando del why, guardar la salida en el run dir. p2: localizar dónde el rollback restaura el conjunto sucio en memoria y hacer que restaure también el persistido (o que la persistencia ocurra solo al confirmar la transacción). p3: correr tests/api completo con -n 4 y tests/store/test_merkle_operation_cache.py. p4: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo. La puerta 'identidad' de check.sh --fast en rojo por workbench_demo es la excepción autorizada (f055723d).

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider -n 4 tests/api tests/store/test_merkle_operation_cache.py

## Done When

_Name the observable condition that makes the task complete._

python -m pytest -q -n 4 tests/api da 0 fallas y tests/store/test_merkle_operation_cache.py pasa.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-4ea8e4d4dc22`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-4ea8e4d4dc22

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
