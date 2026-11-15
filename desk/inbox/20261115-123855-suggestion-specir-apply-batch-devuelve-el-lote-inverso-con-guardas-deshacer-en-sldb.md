---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-15T12:38:55'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# [specIR] apply_batch devuelve el lote inverso con guardas (deshacer en sldb)

_Describe the incoming message with enough evidence to triage._

Pedido concreto que reemplaza la forma abierta de la fila 11 de IR01 (sldb:20261114-074447-suggestion-specir-brechas-api-p-blica-sldb-para-mcp). JP decidió el 2026-11-15 que deshacer es de sldb, no de los consumidores.

Pedido: que sldb.api.apply_batch devuelva en BatchReport el lote inverso de lo que aplicó, en la misma forma que acepta apply_batch:
- crear X → borrar X;
- actualizar X → restaurar los campos o el texto previos de X;
- borrar X → recrear X con su contenido previo;
- aristas: lo mismo sobre sus RelationDoc.
Cada operación del inverso lleva expected_source_hash del estado que dejó el lote, así que aplicar el inverso después de que alguien tocó X se rechaza como ConflictError, sin escritura parcial. Deshacer = apply_batch(report.inverse). La procedencia del inverso queda registrada como cualquier escritura.

Consumidores: specIR (tool MCP undo_changes, que solo guarda los inversos de la sesión y los reaplica), deskops y la UI.

Pregunta al desk: ¿puede exponerse así, o hay una forma mejor dentro de Transaction (que ya tiene los snapshots para el rollback)?
TaskDoc consumidor: task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas
