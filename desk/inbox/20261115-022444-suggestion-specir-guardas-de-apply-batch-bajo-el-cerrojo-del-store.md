---
sldb:
  by: agent
  at: '2026-11-16T08:20:43Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-15T02:24:44'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:20:27'
---

# [specIR] guardas de apply_batch bajo el cerrojo del store

_Describe the incoming message with enough evidence to triage._

Necesidad: el MCP de specIR protege la aplicación con guardas expected_source_hash por documento (decisión IR02 D2, JP 2026-11-15). Revisado en sldb a3514755: apply_batch comprueba los guardas en prevalidate_changes (batch_prevalidate.check_guards) y luego aplica con _APPLY['update'] = tx.update(id, payload), sin pasar los guardas; el cerrojo StoreIOLock (src/sldb/store/io/lock.py, store_lock) se toma por escritura de índice (payload_save_steps.py:105, untrack_document.py:61), no sobre toda la prevalidación+aplicación. Con dos procesos escribiendo, otro puede cambiar un documento entre la comprobación y la escritura y el guarda no lo ve. Pedido: que apply_batch sostenga store_lock desde la prevalidación hasta el fin de la transacción, o que vuelva a verificar expected_source_hash/expected dentro de la transacción (pasándolos a tx.update/delete/move) bajo ese cerrojo; reusar StoreIOLock, sin cerrojo nuevo. Relacionado con la brecha de store_hash atómico ya pedida en sldb:20261114-074447-suggestion-specir-brechas-api-p-blica-sldb-para-mcp. TaskDoc: task-ir02-decisión-contrato-de-escritura-y-nivel-de-mutabilidad-del-mcp
