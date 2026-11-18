---
sldb:
  by: agent
  at: '2026-11-18T23:14:58Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-17T13:53:38'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-18T20:14:36'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'Convertida en tarea de sldb (undo_changes: guard stale sin procedencia,
  steps=N atómico, contrato ''mismo contenido salvo procedencia'').'
---

# IR04b: undo_changes de sldb mcp falla tras re-sellar procedencia (stale imposible de satisfacer, steps=2 escribe a medias)

_Describe the incoming message with enough evidence to triage._

IR04b verificó desde specIR el undo_changes de sldb mcp (d0ee07a3) con un cliente MCP real sobre una copia montada del store. Evidencia: IR/runs/subagents/deskops-e-674fcb14989b-a2/ (result-summary.md, undo-run3.log, tests/test_mcp_undo.py en el árbol de IR, sin commit). Lo que cumple: nivel 0 sin tools; nivel 1 rechaza un lote con RuleDoc en propose y no deshace uno de nivel 2; nivel 2 deshace RuleDoc; rules check y edges check rc 0 tras el undo. Hallazgos: (1) El undo devuelve el contenido pero re-sella la procedencia: el .md cambia sldb.at, el índice del documento cambia source_hash, at y via (create_document -> save_document_payload), los modelos cambian sections_index o model_hash/roster_hash y store_index cambia store_hash. La copia no queda idéntica. Pregunta: ¿es el contrato de undo 'mismo contenido salvo procedencia'? Si lo es, specIR relaja su validación; si no, es un defecto. (2) Defecto: el guard stale compara source_hash, que incluye la procedencia re-sellada. Tras un cambio ajeno por sldb.api.apply_batch y su reversión al contenido anterior, undo_changes sigue en {applied: False, rejected: stale, document: undo-seed-op, expected 213c32e8..., found 4baced0e..., remaining: 1}: ningún lote puede satisfacerlo y el lote queda atascado en la pila. (3) Defecto de atomicidad: con dos lotes donde el segundo edita un documento del primero, undo_changes(steps=2) responde {applied: False, rejected: stale, written: True}: escribió el inverso del segundo y rechazó el del primero, porque el primero espera el hash anterior al segundo. Un rechazo no debería dejar escrito nada, o los pasos deberían encadenarse. IR04b queda bloqueada hasta vuestra respuesta. Respetando la pausa de JP: es solo aviso, sin urgencia.
