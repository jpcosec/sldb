---
sldb:
  by: agent
  at: '2026-11-19T06:48:09Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-check-edges-clasifica-como-stale-propio-los-de-stores-enlazados-cuyo-nombre-lleva-dos-puntos-inbox-2-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-check-edges-clasifica-como-stale-propio-los-de-stores-enlazados-cuyo-nombre-lleva-dos-puntos-inbox-2@sha256:5ab7840f04ac7081cba5a12728c2e398a3e711e0605870a9a4bea143a80c0b65
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261119-064614/context-review/task-check-edges-clasifica-como-stale-propio-los-de-stores-enlazados-cuyo-nombre-lleva-dos-puntos-inbox-2/bundle/8ff9aff9f21e118512ccf4d40f0b8ec61c3fd8f2086ba0c74678af56e65d15c8/attempt-1
input_sha256: 8ff9aff9f21e118512ccf4d40f0b8ec61c3fd8f2086ba0c74678af56e65d15c8
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 826440566f9061ab53db9b30dac2d93d8bd0c8fac41ce1ec829277d1b92f4fab
output_sha256: 5302ffa143edaa243e7ee38a5913c6aac7a9ba3c3fa6b6eb139f9cfda027f3ae
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador: 1) Se usa el dato de dueño que ya
  llegue a index.stale sin cambiar el formato de los ids: primero from_store (qualify
  lo pone en cada contribución enlazada); si no llega a stale, los nombres de los
  stores enlazados del índice. El ejecutor dice en el informe cuál usó, con archivo
  y línea. 2) Caché frío es sin .sldb_cache (directorio borrado antes de la llamada)
  y caché caliente es la segunda llamada; el test cubre los dos. 3) Commit con el
  trailer ''Task-Id: <id de la tarea>'' y rutas nombradas. 4) stores build --check
  no es gate de esta tarea (lo corre el CI); manda la sección Validation. 5) HEAD
  es main de sldb al despachar. Bundle: 1) el fixture lleva un documento propio con
  exactamente un '':'' en el nombre (id ''Model:a:b'', que hoy cuenta como enlazado)
  y uno enlazado con un '':'' en el nombre (''store:Model:a:b'', que hoy cuenta como
  propio). 2) Ver la resolución 1. 3) Ver la 4. 4) La evidencia es runs/subagents/20261119-repro-check-edges/
  (repro.md y regla.txt), en el repo; el directorio context-review es el de la propia
  revisión.'
# ISO 8601 timestamp
created_at: '2026-11-19T06:46:26.187217+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T06:47:48.287284+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-check-edges-clasifica-como-stale-propio-los-de-stores-enlazados-cuyo-nombre-lleva-dos-puntos-inbox-2

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261119-064614/context-review/task-check-edges-clasifica-como-stale-propio-los-de-stores-enlazados-cuyo-nombre-lleva-dos-puntos-inbox-2/bundle/8ff9aff9f21e118512ccf4d40f0b8ec61c3fd8f2086ba0c74678af56e65d15c8/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador: 1) Se usa el dato de dueño que ya llegue a index.stale sin cambiar el formato de los ids: primero from_store (qualify lo pone en cada contribución enlazada); si no llega a stale, los nombres de los stores enlazados del índice. El ejecutor dice en el informe cuál usó, con archivo y línea. 2) Caché frío es sin .sldb_cache (directorio borrado antes de la llamada) y caché caliente es la segunda llamada; el test cubre los dos. 3) Commit con el trailer 'Task-Id: <id de la tarea>' y rutas nombradas. 4) stores build --check no es gate de esta tarea (lo corre el CI); manda la sección Validation. 5) HEAD es main de sldb al despachar. Bundle: 1) el fixture lleva un documento propio con exactamente un ':' en el nombre (id 'Model:a:b', que hoy cuenta como enlazado) y uno enlazado con un ':' en el nombre ('store:Model:a:b', que hoy cuenta como propio). 2) Ver la resolución 1. 3) Ver la 4. 4) La evidencia es runs/subagents/20261119-repro-check-edges/ (repro.md y regla.txt), en el repo; el directorio context-review es el de la propia revisión.
