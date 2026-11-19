---
sldb:
  by: agent
  at: '2026-11-19T10:46:07Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-docs-track-reindex-re-indexa-un-documento-ya-trackeado-validándolo-sin-saltar-el-round-trip-como-for-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-docs-track-reindex-re-indexa-un-documento-ya-trackeado-validándolo-sin-saltar-el-round-trip-como-for@sha256:18a15c851f96bef0e1c1a20451ab6859ce07777ee63869dab4cbb6bb5ba0c600
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261119-104409/context-review/task-docs-track-reindex-re-indexa-un-documento-ya-trackeado-validándolo-sin-saltar-el-round-trip-como-for/bundle/11efc39b55d1e91c09d1842a82b0c71ca8ab9efef6c6a6a67865017ea84dd7d3/attempt-1
input_sha256: 11efc39b55d1e91c09d1842a82b0c71ca8ab9efef6c6a6a67865017ea84dd7d3
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: fae17780bc355d96dbe6c91f1c4d00f0e28b143aa0451a2820d0e0229aa00673
output_sha256: 0774ee12f6f641e23a339833b42a0fc2929bf7d2cec30eb34d5c8a0ac35ec7fa
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador: 1) El camino de force de CI2 es el
  de StoreOperations.track en src/sldb/store/ops.py, el que agregó ''docs track --force''
  (commit f3d51b29, re-track con force). --reindex lo reusa para re-indexar. 2) y
  3) --reindex corre las mismas validaciones que track sin force (round-trip del modelo,
  refuse_structural_noise, refuse_undeclared_frontmatter y las que ya llame track_document_file
  en ese camino), antes de escribir. Si alguna falla, no se escribe nada y no hace
  falta rollback. ''Byte a byte'' compara todos los archivos bajo .sldb/core/ y .sldb/store.yaml
  antes y después. 4) --reindex sobre un documento no trackeado es exactamente track
  sin force. 5) El aviso a sldb-ui lo manda el integrador tras integrar. 6) Commit
  con trailer ''Task-Id: <id de la tarea>'' y rutas nombradas. Bundle: --reindex y
  --force van en un grupo mutuamente excluyente de argparse, así que el error es el
  de argparse con exit 2; el handler del comando está en src/sldb/cli/commands/docs.py
  (o el módulo docs_* que lo despache, que el ejecutor cita).'
# ISO 8601 timestamp
created_at: '2026-11-19T10:44:24.022068+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T10:45:46.805901+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-docs-track-reindex-re-indexa-un-documento-ya-trackeado-validándolo-sin-saltar-el-round-trip-como-for

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261119-104409/context-review/task-docs-track-reindex-re-indexa-un-documento-ya-trackeado-validándolo-sin-saltar-el-round-trip-como-for/bundle/11efc39b55d1e91c09d1842a82b0c71ca8ab9efef6c6a6a67865017ea84dd7d3/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador: 1) El camino de force de CI2 es el de StoreOperations.track en src/sldb/store/ops.py, el que agregó 'docs track --force' (commit f3d51b29, re-track con force). --reindex lo reusa para re-indexar. 2) y 3) --reindex corre las mismas validaciones que track sin force (round-trip del modelo, refuse_structural_noise, refuse_undeclared_frontmatter y las que ya llame track_document_file en ese camino), antes de escribir. Si alguna falla, no se escribe nada y no hace falta rollback. 'Byte a byte' compara todos los archivos bajo .sldb/core/ y .sldb/store.yaml antes y después. 4) --reindex sobre un documento no trackeado es exactamente track sin force. 5) El aviso a sldb-ui lo manda el integrador tras integrar. 6) Commit con trailer 'Task-Id: <id de la tarea>' y rutas nombradas. Bundle: --reindex y --force van en un grupo mutuamente excluyente de argparse, así que el error es el de argparse con exit 2; el handler del comando está en src/sldb/cli/commands/docs.py (o el módulo docs_* que lo despache, que el ejecutor cita).
