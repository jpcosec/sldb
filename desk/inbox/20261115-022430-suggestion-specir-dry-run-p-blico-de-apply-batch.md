---
sldb:
  by: agent
  at: '2026-11-16T08:20:23Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-15T02:24:30'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:20:08'
---

# [specIR] dry_run público de apply_batch

_Describe the incoming message with enough evidence to triage._

Necesidad: el MCP de specIR (decisión IR02 D1, docs/decisiones/contrato-de-escritura-mcp.md en IR, JP 2026-11-15) valida una propuesta de cambio como lote de apply_batch SIN escribir, y luego la aplica igual. Revisado en sldb a3514755: sldb.api.apply_batch (src/sldb/api/documents/apply_batch.py) no tiene dry_run; su prevalidación es sldb.api.documents.batch_prevalidate.prevalidate_changes, que no está en sldb.api.__all__ y recibe un StoreLocation. Pedido: un modo de validar sin escribir en la API pública, p. ej. apply_batch(store, changes, dry_run=True) que corra prevalidate_changes (forma, modelo, round-trip G4, guardas, destinos) y devuelva el informe o los errores, sin abrir transacción. Alternativa aceptable: re-exportar prevalidate_changes con una firma pública por store. specIR no importará el módulo interno mientras no sea público. TaskDoc: task-ir02-decisión-contrato-de-escritura-y-nivel-de-mutabilidad-del-mcp
