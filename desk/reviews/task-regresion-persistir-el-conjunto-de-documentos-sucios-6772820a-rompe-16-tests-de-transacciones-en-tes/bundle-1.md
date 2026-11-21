---
sldb:
  by: agent
  at: '2026-11-21T12:51:29Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes@sha256:9219235e9876d0ece54b143beb1eea05ad5581544c972a3229db218160379338
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261121-124812/context-review/task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes/bundle/7d9a8402fafd9a60c4d69b955cde1eda2de9d56f6734991c3baecc7f4de5b024/attempt-1
input_sha256: 7d9a8402fafd9a60c4d69b955cde1eda2de9d56f6734991c3baecc7f4de5b024
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: b92e842a8c10fd61b36fb6fe17cebf33d2633cc54857e8e57adeddae1f3adbf8
output_sha256: 86d85fa4e02f20b6e317584abac8962b7090a847bad1d1d691ccaf18e97a3c32
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador.


  P1, P2 y B5) El universo exacto son los 16 tests de tests/api que fallan hoy sobre
  main local y pasan sobre origin/main. La línea base verde es origin/main, donde
  tests/api da 643 passed y 32 skipped. Para listarlos: python -m pytest -q -p no:cacheprovider
  -n 4 tests/api | grep ^FAILED. Los ''9 failed'' son el subconjunto de los tres archivos
  del comando de reproducción. Tienen que pasar los 16, y tests/api completo tiene
  que dar 0 fallas.


  P3 y B1) Se agrega un test nuevo solo si el arreglo cambia un comportamiento que
  ningún test existente cubre. Si los 16 vuelven a verde y tests/store/test_merkle_operation_cache.py
  pasa, no hace falta ninguno.


  P4) Superficie concreta:

  - src/sldb/api/documents/transaction_state.py, que toma la instantánea del conjunto
  sucio de reglas al entrar en la transacción (docstring, línea 23);

  - src/sldb/store/io/rollback.py;

  - src/sldb/store/documents_dirty.py;

  - src/sldb/store/documents_dirty_persist.py.


  B2) Criterio de elección: preferir que la persistencia a disco ocurra solo al confirmar
  la transacción, o fuera de ella. Si eso rompe el modo incremental entre procesos
  (test_merkle_operation_cache), restaurar el persistido en el rollback junto con
  la instantánea en memoria. Gana la opción que deje los dos conjuntos de tests en
  verde con menos código.


  P5 y B4) check.sh --fast (bash tools/check.sh --fast) es una puerta del desk, no
  de la Validation de la tarea. Se corre; el rojo de ''identidad'' por el directorio
  workbench_demo es la excepción autorizada (decisión f055723d); cualquier otra puerta
  en rojo bloquea.


  P6 y B3) El worktree es el que dispatch le da al ejecutor (lo dice su prompt). El
  trailer es ''Task-Id: <id de esta tarea>'' en el cuerpo.


  B6) La tarea no tiene pills ni átomos ligados. Se trabaja con el TaskDoc solo.


  B7) Prevalece el TaskDoc: no se cambian los asserts de tests/api, porque esos tests
  describen el comportamiento correcto (pasan en origin).'
# ISO 8601 timestamp
created_at: '2026-11-21T12:48:29.522512+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T12:51:07.078244+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261121-124812/context-review/task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes/bundle/7d9a8402fafd9a60c4d69b955cde1eda2de9d56f6734991c3baecc7f4de5b024/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador.

P1, P2 y B5) El universo exacto son los 16 tests de tests/api que fallan hoy sobre main local y pasan sobre origin/main. La línea base verde es origin/main, donde tests/api da 643 passed y 32 skipped. Para listarlos: python -m pytest -q -p no:cacheprovider -n 4 tests/api | grep ^FAILED. Los '9 failed' son el subconjunto de los tres archivos del comando de reproducción. Tienen que pasar los 16, y tests/api completo tiene que dar 0 fallas.

P3 y B1) Se agrega un test nuevo solo si el arreglo cambia un comportamiento que ningún test existente cubre. Si los 16 vuelven a verde y tests/store/test_merkle_operation_cache.py pasa, no hace falta ninguno.

P4) Superficie concreta:
- src/sldb/api/documents/transaction_state.py, que toma la instantánea del conjunto sucio de reglas al entrar en la transacción (docstring, línea 23);
- src/sldb/store/io/rollback.py;
- src/sldb/store/documents_dirty.py;
- src/sldb/store/documents_dirty_persist.py.

B2) Criterio de elección: preferir que la persistencia a disco ocurra solo al confirmar la transacción, o fuera de ella. Si eso rompe el modo incremental entre procesos (test_merkle_operation_cache), restaurar el persistido en el rollback junto con la instantánea en memoria. Gana la opción que deje los dos conjuntos de tests en verde con menos código.

P5 y B4) check.sh --fast (bash tools/check.sh --fast) es una puerta del desk, no de la Validation de la tarea. Se corre; el rojo de 'identidad' por el directorio workbench_demo es la excepción autorizada (decisión f055723d); cualquier otra puerta en rojo bloquea.

P6 y B3) El worktree es el que dispatch le da al ejecutor (lo dice su prompt). El trailer es 'Task-Id: <id de esta tarea>' en el cuerpo.

B6) La tarea no tiene pills ni átomos ligados. Se trabaja con el TaskDoc solo.

B7) Prevalece el TaskDoc: no se cambian los asserts de tests/api, porque esos tests describen el comportamiento correcto (pasan en origin).
