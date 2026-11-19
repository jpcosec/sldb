---
sldb:
  by: agent
  at: '2026-11-19T06:47:40Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-check-edges-clasifica-como-stale-propio-los-de-stores-enlazados-cuyo-nombre-lleva-dos-puntos-inbox-2-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
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
run_dir: runs/subagents/20261119-064537/context-review/task-check-edges-clasifica-como-stale-propio-los-de-stores-enlazados-cuyo-nombre-lleva-dos-puntos-inbox-2/preflight/d16593c98e533e486562f5840369c8b66156d8c9a45daca5e9396467a961b036/attempt-1
input_sha256: d16593c98e533e486562f5840369c8b66156d8c9a45daca5e9396467a961b036
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 2508e6f696b48751ce9651e272a5e0609afe9c5eba3167063872bad29185b9a1
output_sha256: ed7120e248f92d6f3801551ff3d51ef8c3ee7a783d48aa63a22b5122949a07e1
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
created_at: '2026-11-19T06:45:47.839550+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T06:47:18.975846+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-check-edges-clasifica-como-stale-propio-los-de-stores-enlazados-cuyo-nombre-lleva-dos-puntos-inbox-2

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261119-064537/context-review/task-check-edges-clasifica-como-stale-propio-los-de-stores-enlazados-cuyo-nombre-lleva-dos-puntos-inbox-2/preflight/d16593c98e533e486562f5840369c8b66156d8c9a45daca5e9396467a961b036/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador: 1) Se usa el dato de dueño que ya llegue a index.stale sin cambiar el formato de los ids: primero from_store (qualify lo pone en cada contribución enlazada); si no llega a stale, los nombres de los stores enlazados del índice. El ejecutor dice en el informe cuál usó, con archivo y línea. 2) Caché frío es sin .sldb_cache (directorio borrado antes de la llamada) y caché caliente es la segunda llamada; el test cubre los dos. 3) Commit con el trailer 'Task-Id: <id de la tarea>' y rutas nombradas. 4) stores build --check no es gate de esta tarea (lo corre el CI); manda la sección Validation. 5) HEAD es main de sldb al despachar. Bundle: 1) el fixture lleva un documento propio con exactamente un ':' en el nombre (id 'Model:a:b', que hoy cuenta como enlazado) y uno enlazado con un ':' en el nombre ('store:Model:a:b', que hoy cuenta como propio). 2) Ver la resolución 1. 3) Ver la 4. 4) La evidencia es runs/subagents/20261119-repro-check-edges/ (repro.md y regla.txt), en el repo; el directorio context-review es el de la propia revisión.
