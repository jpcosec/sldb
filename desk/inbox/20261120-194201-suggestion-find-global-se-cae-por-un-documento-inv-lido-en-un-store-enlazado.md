---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: repo-governance
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-20T19:42:01'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# find --global se cae por un documento inválido en un store enlazado

_Describe the incoming message with enough evidence to triage._

Desde Governance, que enlaza los stores de 14 desks: sldb find <término> --global --store .sldb termina con «Unexpected: 1 validation error for TaskDoc» porque un store enlazado (shared_llm-gateway) tiene una tarea con estado incoherente (task-ci-propio-del-gateway: superseded con historial vacío). Un documento inválido en un desk deja ciego al desk que coordina. load_runtime_documents ya tiene los parámetros rejected y accepted_only; pedido: que la lectura federada salte el documento inválido, lo informe con su store y siga.
