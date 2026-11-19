---
sldb:
  by: agent
  at: '2026-11-19T05:45:15Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
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
run_dir: runs/subagents/20261119-054257/context-review/task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do/preflight/fbee6d884772ace83535eff6e2020f35fb56e8b4808826519151b7e072952f08/attempt-1
input_sha256: fbee6d884772ace83535eff6e2020f35fb56e8b4808826519151b7e072952f08
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 136f900c1ab77a6e0254da9fa6dcc515270a884da0e648c2da6ecd2138973ed1
output_sha256: ae18ccd4217aa7db9247a7e39eea7c8e971bb0c24dfbd9b1942603a91c012a9f
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
created_at: '2026-11-19T05:43:08.329114+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T05:44:53.151408+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261119-054257/context-review/task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do/preflight/fbee6d884772ace83535eff6e2020f35fb56e8b4808826519151b7e072952f08/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador: 1) La fuente real de cada uno la encuentra el ejecutor leyendo src/sldb/cli/commands/docs.py y la API que llaman (p1), y la cita con archivo y línea; store_index.yaml es una candidata, no un supuesto. 2) Se prefiere que list y show coincidan, sea porque list deja fuera lo que show no resuelve o porque show resuelve lo que list lista. Si hace falta marcar: en JSON cada entrada gana 'resolvable': false y 'reason': '<causa>'; en texto, la línea agrega ' (no resoluble: <causa>)'. 3) El test cubre el caso observado (un documento derivado, como la arista edge-task-…-to-activate, listado pero ausente del índice); el declarado es opcional. 4) La API está en este repo, src/sldb/api (test de referencia tests/api/test_select_documents.py). 5) El aviso a sldb-ui lo manda el integrador después de integrar; el ejecutor no avisa. 6) El informe va en result-summary.md del run dir que fija dispatch. Bundle: pills y atoms vacíos está bien; no hace falta material extra.
