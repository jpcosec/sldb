---
sldb:
  by: agent
  at: '2026-11-17T06:38:21Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-17T02:15:15'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T03:37:55'
---

# read_store dice 'store not prepared' para un store inexistente

_Describe the incoming message with enough evidence to triage._

sldb.api.read_store (origin/main d50dd6a9, src/sldb/api/stores/read_store.py) lanza SLDBStoreError 'store not prepared: run `sldb stores update` (<ruta>)' también cuando el store NO existe, porque store_is_prepared devuelve False si falta .sldb o core/store_index.yaml. Correr 'sldb stores update' no sirve en ese caso. En graph_ui (commit d62195c) un POST /api/save con .sldb borrado responde 503 'store not prepared', y el operador queda mal guiado. Lo vio el tester independiente: runs/subagents/20261117-viewsave-tester-a1/result-summary.md, hallazgo O1. Pedido: distinguir el store inexistente con otro mensaje, por ejemplo 'store not found: <ruta>' (sldb ya lo usa en _resolve_store_arg para alias). graph_ui solo traduce a 503 la substring 'store not prepared'; un mensaje distinto le llegaría como el error genérico que corresponda.
