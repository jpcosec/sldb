---
sldb:
  by: agent
  at: '2026-11-20T03:16:34Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-arreglo-de-3f547569-cache-vieja-de-reviewdoc-layout-py-pasa-el-limite-de-80-lineas-y-el-test-de-rees-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-arreglo-de-3f547569-cache-vieja-de-reviewdoc-layout-py-pasa-el-limite-de-80-lineas-y-el-test-de-rees@sha256:1a08fa8cfe226123c72d7cbec2ba6970ad07e330dfac23fa829505fc901c0077
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261120-031434/context-review/task-arreglo-de-3f547569-cache-vieja-de-reviewdoc-layout-py-pasa-el-limite-de-80-lineas-y-el-test-de-rees/bundle/e9a3fcd71434fad242e9d41f2e54597812e58ef6d6df7860a7cad5752d95426f/attempt-1
input_sha256: e9a3fcd71434fad242e9d41f2e54597812e58ef6d6df7860a7cad5752d95426f
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 69f215652b2722cbe2c7b806cdf23e42dffabdd40434d8b86d5767fdee189d7c
output_sha256: 24dfbbbad0eb2279c7a8e37e2fcdfee9a689263e78f7fe593c93a23703983913
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador: 1) drop_disk_caches va a un módulo
  nuevo, src/sldb/store/disk_caches.py, con su import en build_store.py; layout.py
  vuelve a dejar solo rutas. 2) y bundle 2) La culpable la determina el ejecutor,
  que corre el test fallido con un print o un breakpoint para ver cuál caché devuelve
  la fila vieja: la compuesta (src/sldb/store/edge_index/composed_disk.py) o la de
  filas (src/sldb/store/query_engine/document_rows_disk.py). ''Ver el roster'' significa
  que su clave incluye roster_state(p) de src/sldb/store/edge_index/cache_keys.py
  para cada store, como ya hace la compuesta desde 3f547569. Si las dos lo necesitan,
  se aplica en las dos. 3) Ruta completa: src/sldb/store/edge_index/composed_disk.py.
  4) y bundle 5) Dos comprobaciones: (a) ''for i in $(seq 20); do TMPDIR=/tmp python
  -m pytest -q -p no:cacheprovider tests/api/test_select_documents_disk.py || break;
  done'', 20 seguidas en verde; (b) ''TMPDIR=/tmp python -m pytest -q -p no:cacheprovider
  -n 4 tests/api/'' en verde. Los logs van al run_dir. 5) El test es la especificación:
  una reescritura in place dentro del mismo tick tiene que verse en el siguiente proceso.
  No se cambian sus asserts ni se agrega sleep; si resultara imposible, el ejecutor
  lo informa con evidencia en vez de cambiarlo. Bundle 3) El ejecutor corre (a) y
  (b), test_clean_code_rules y tools/check.sh --fast; la suite completa la corre integrate.
  Bundle 4) La matriz es (a) y (b). Commit con trailer ''Task-Id: <id de esta tarea>''
  y rutas nombradas.'
# ISO 8601 timestamp
created_at: '2026-11-20T03:14:53.925275+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T03:16:12.540657+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-arreglo-de-3f547569-cache-vieja-de-reviewdoc-layout-py-pasa-el-limite-de-80-lineas-y-el-test-de-rees

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261120-031434/context-review/task-arreglo-de-3f547569-cache-vieja-de-reviewdoc-layout-py-pasa-el-limite-de-80-lineas-y-el-test-de-rees/bundle/e9a3fcd71434fad242e9d41f2e54597812e58ef6d6df7860a7cad5752d95426f/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador: 1) drop_disk_caches va a un módulo nuevo, src/sldb/store/disk_caches.py, con su import en build_store.py; layout.py vuelve a dejar solo rutas. 2) y bundle 2) La culpable la determina el ejecutor, que corre el test fallido con un print o un breakpoint para ver cuál caché devuelve la fila vieja: la compuesta (src/sldb/store/edge_index/composed_disk.py) o la de filas (src/sldb/store/query_engine/document_rows_disk.py). 'Ver el roster' significa que su clave incluye roster_state(p) de src/sldb/store/edge_index/cache_keys.py para cada store, como ya hace la compuesta desde 3f547569. Si las dos lo necesitan, se aplica en las dos. 3) Ruta completa: src/sldb/store/edge_index/composed_disk.py. 4) y bundle 5) Dos comprobaciones: (a) 'for i in $(seq 20); do TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_select_documents_disk.py || break; done', 20 seguidas en verde; (b) 'TMPDIR=/tmp python -m pytest -q -p no:cacheprovider -n 4 tests/api/' en verde. Los logs van al run_dir. 5) El test es la especificación: una reescritura in place dentro del mismo tick tiene que verse en el siguiente proceso. No se cambian sus asserts ni se agrega sleep; si resultara imposible, el ejecutor lo informa con evidencia en vez de cambiarlo. Bundle 3) El ejecutor corre (a) y (b), test_clean_code_rules y tools/check.sh --fast; la suite completa la corre integrate. Bundle 4) La matriz es (a) y (b). Commit con trailer 'Task-Id: <id de esta tarea>' y rutas nombradas.
