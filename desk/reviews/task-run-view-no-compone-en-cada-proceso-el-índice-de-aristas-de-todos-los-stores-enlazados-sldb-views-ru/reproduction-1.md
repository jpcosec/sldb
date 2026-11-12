---
sldb:
  by: agent
  at: '2026-11-12T02:26:38Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-run-view-no-compone-en-cada-proceso-el-índice-de-aristas-de-todos-los-stores-enlazados-sldb-views-ru-reproduction-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: reproduction
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-run-view-no-compone-en-cada-proceso-el-índice-de-aristas-de-todos-los-stores-enlazados-sldb-views-ru
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: human
actor: coord2
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: a3d5625e1280510104e248726648a635b2b1f9c62faf09cdb2fc06edd880aa34
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: pending
reason: 'Reproducido sobre deskops d120766d con sldb b965c62d (layout en /dev/shm,
  stores enlazados sldb, spec2viz y scion, store de deskops construido, XDG cache
  vacío): deskops view board tarda 9,4 s y 9,7 s en procesos nuevos; el perfil de
  run_view da 10,89 s, de los cuales 8,90 s en load_edge_index y compose_edge_index
  (4 stores, 5067 shards, 4606 yaml.load). A escala real el informe de CC34 midió
  38,4 s.'
# ISO 8601 timestamp
created_at: '2026-11-12T02:26:37.721313+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: ''
disposed_by: ''
# e.g. workspace:desk
tags:
- workspace:desk
---

# Reproduction review of task-run-view-no-compone-en-cada-proceso-el-índice-de-aristas-de-todos-los-stores-enlazados-sldb-views-ru

## Summary

_Summarize what was reviewed and the evidence this receipt records._

reproduction receipt recorded by coord2; evidence: runs/subagents/20261112-repro-h11/repro.log

## Disposition

_Record the verdict rationale and who disposed of the review._
