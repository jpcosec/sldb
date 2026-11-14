---
sldb:
  by: agent
  at: '2026-11-12T03:38:14Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-sldb-views-run-board-en-menos-de-1-s-caché-de-disco-de-los-shards-de-documentos-para-select-document-reproduction-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: reproduction
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-sldb-views-run-board-en-menos-de-1-s-caché-de-disco-de-los-shards-de-documentos-para-select-document
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: human
actor: coord2
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: a4afab9961c2311e2dd1c22ea2090fe79dbf8bd166310810c51c184a759a5c28
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: pending
reason: 'Mediciones del h11-worker (mediana de 3, proceso nuevo, carga 11-13): con
  H11 aplicada, sldb views run board da 1,59 s con la caché de composición caliente
  y 3,9 s en la primera corrida tras el build; desglose del caliente: importar sldb.api
  ~0,55 s, índice JSON ~0,38 s, select_documents ~0,35 s (parsea ~540 shards de documentos
  con yaml). El coordinador no las re-corrió por la carga de la máquina; el worker
  de la tarea mide su línea base propia con caché frío y caliente.'
# ISO 8601 timestamp
created_at: '2026-11-12T03:38:14.232544+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: ''
disposed_by: ''
# e.g. workspace:desk
tags:
- workspace:desk
---

# Reproduction review of task-sldb-views-run-board-en-menos-de-1-s-caché-de-disco-de-los-shards-de-documentos-para-select-document

## Summary

_Summarize what was reviewed and the evidence this receipt records._

reproduction receipt recorded by coord2; evidence: runs/subagents/20261112-repro-h11b/repro.log

## Disposition

_Record the verdict rationale and who disposed of the review._
