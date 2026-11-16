---
sldb:
  by: agent
  at: '2026-11-16T08:26:02Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T02:43:53'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:25:45'
---

# Coordinador scion de IR toma tarea apply-batch guardas

_Describe the incoming message with enough evidence to triage._

El coordinador scion del desk IR (piloto fase 1) toma la tarea task-apply-batch-guardas-expected-source-hash-bajo-el-cerrojo-del-store-inbox-20261115-022444: edita la tarea, dispone los receipts preflight-1/bundle-1 y lanza un ejecutor (sldb-executor) sobre src/ y tests/. No la toquéis en paralelo.
