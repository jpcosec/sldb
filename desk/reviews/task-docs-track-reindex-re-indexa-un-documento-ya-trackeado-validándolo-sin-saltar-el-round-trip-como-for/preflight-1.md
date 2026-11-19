---
sldb:
  by: agent
  at: '2026-11-19T10:45:38Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-docs-track-reindex-re-indexa-un-documento-ya-trackeado-validándolo-sin-saltar-el-round-trip-como-for-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
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
run_dir: runs/subagents/20261119-104330/context-review/task-docs-track-reindex-re-indexa-un-documento-ya-trackeado-validándolo-sin-saltar-el-round-trip-como-for/preflight/5e4ce8c70fe0c0e9fd0c989be045be2a6006bc729d337f1a8609c8d08ee863e1/attempt-1
input_sha256: 5e4ce8c70fe0c0e9fd0c989be045be2a6006bc729d337f1a8609c8d08ee863e1
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ef0f633719f71b294d7f288a3081e7a356200459d92547d81d1da2a125846ccd
output_sha256: 32f3074ea20d05c3ae3bd079f8da5653ff884875fc42253ca56782a450badcc3
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
created_at: '2026-11-19T10:43:42.330202+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T10:45:17.722714+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-docs-track-reindex-re-indexa-un-documento-ya-trackeado-validándolo-sin-saltar-el-round-trip-como-for

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261119-104330/context-review/task-docs-track-reindex-re-indexa-un-documento-ya-trackeado-validándolo-sin-saltar-el-round-trip-como-for/preflight/5e4ce8c70fe0c0e9fd0c989be045be2a6006bc729d337f1a8609c8d08ee863e1/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador: 1) El camino de force de CI2 es el de StoreOperations.track en src/sldb/store/ops.py, el que agregó 'docs track --force' (commit f3d51b29, re-track con force). --reindex lo reusa para re-indexar. 2) y 3) --reindex corre las mismas validaciones que track sin force (round-trip del modelo, refuse_structural_noise, refuse_undeclared_frontmatter y las que ya llame track_document_file en ese camino), antes de escribir. Si alguna falla, no se escribe nada y no hace falta rollback. 'Byte a byte' compara todos los archivos bajo .sldb/core/ y .sldb/store.yaml antes y después. 4) --reindex sobre un documento no trackeado es exactamente track sin force. 5) El aviso a sldb-ui lo manda el integrador tras integrar. 6) Commit con trailer 'Task-Id: <id de la tarea>' y rutas nombradas. Bundle: --reindex y --force van en un grupo mutuamente excluyente de argparse, así que el error es el de argparse con exit 2; el handler del comando está en src/sldb/cli/commands/docs.py (o el módulo docs_* que lo despache, que el ejecutor cita).
