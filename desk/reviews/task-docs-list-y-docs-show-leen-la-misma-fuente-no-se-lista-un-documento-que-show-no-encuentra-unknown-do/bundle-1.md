---
sldb:
  by: agent
  at: '2026-11-19T05:45:46Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do@sha256:82a0ef1cd7975ea2ca95a1be60da43e8bad02f0410dbdf5f2919174a92bc9e5d
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261119-054335/context-review/task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do/bundle/66d1d268589c49114f1a5fc2fb18689c949bfd7deafcbbf94c86560b48492ff5/attempt-1
input_sha256: 66d1d268589c49114f1a5fc2fb18689c949bfd7deafcbbf94c86560b48492ff5
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: a3209b409ae0e31ba4d758f473d5f383600bf61170dc954bc2cb77c4d1656609
output_sha256: d6e6b471b8b7f8518eb8dc333b0f6bf9a6391ede994b348e255cbf2a1dd6890a
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador: 1) La fuente real de cada uno la
  encuentra el ejecutor leyendo src/sldb/cli/commands/docs.py y la API que llaman
  (p1), y la cita con archivo y línea; store_index.yaml es una candidata, no un supuesto.
  2) Se prefiere que list y show coincidan, sea porque list deja fuera lo que show
  no resuelve o porque show resuelve lo que list lista. Si hace falta marcar: en JSON
  cada entrada gana ''resolvable'': false y ''reason'': ''<causa>''; en texto, la
  línea agrega '' (no resoluble: <causa>)''. 3) El test cubre el caso observado (un
  documento derivado, como la arista edge-task-…-to-activate, listado pero ausente
  del índice); el declarado es opcional. 4) La API está en este repo, src/sldb/api
  (test de referencia tests/api/test_select_documents.py). 5) El aviso a sldb-ui lo
  manda el integrador después de integrar; el ejecutor no avisa. 6) El informe va
  en result-summary.md del run dir que fija dispatch. Bundle: pills y atoms vacíos
  está bien; no hace falta material extra.'
# ISO 8601 timestamp
created_at: '2026-11-19T05:43:57.915350+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T05:45:23.147044+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261119-054335/context-review/task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do/bundle/66d1d268589c49114f1a5fc2fb18689c949bfd7deafcbbf94c86560b48492ff5/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador: 1) La fuente real de cada uno la encuentra el ejecutor leyendo src/sldb/cli/commands/docs.py y la API que llaman (p1), y la cita con archivo y línea; store_index.yaml es una candidata, no un supuesto. 2) Se prefiere que list y show coincidan, sea porque list deja fuera lo que show no resuelve o porque show resuelve lo que list lista. Si hace falta marcar: en JSON cada entrada gana 'resolvable': false y 'reason': '<causa>'; en texto, la línea agrega ' (no resoluble: <causa>)'. 3) El test cubre el caso observado (un documento derivado, como la arista edge-task-…-to-activate, listado pero ausente del índice); el declarado es opcional. 4) La API está en este repo, src/sldb/api (test de referencia tests/api/test_select_documents.py). 5) El aviso a sldb-ui lo manda el integrador después de integrar; el ejecutor no avisa. 6) El informe va en result-summary.md del run dir que fija dispatch. Bundle: pills y atoms vacíos está bien; no hace falta material extra.
