---
sldb:
  by: agent
  at: '2026-11-16T08:21:23Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-15T02:26:55'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:21:07'
---

# [specIR] validar aristas antes de escribir y devolver las alertas on_write de apply_batch

_Describe the incoming message with enough evidence to triage._

Detectado en IR04 (escritura por MCP de specIR) sobre sldb b51e9667; verificado que sigue igual en HEAD a3514755. specIR escribe solo con sldb.api.apply_batch y no reimplementa nada de esto. Mientras falte, la tool lo declara como pendiente con el id de esta nota.

1. Validar una arista contra su RelationTypeDoc antes de escribir el RelationDoc. Hoy create_document/save_document_payload/apply_batch escriben un RelationDoc cuyo origen no está en source_types, que rompe la cardinalidad o cuya condición no parsea. Solo check_edges lo detecta, y después de escribir (store/edge_index/validation.py). Repro: apply_batch con un RelationDoc task_activates cuyo source_id es un TaskCodeDoc (source_types ['RitualDoc']) -> saved=[...]; luego check_edges da 'source class TaskCodeDoc not in source_types'. Pedido: en la prevalidación de apply_batch (y en el dry_run pedido en 20261115-022430), y si se puede en create/save, aplicar a los RelationDoc del lote las comprobaciones de validation.py (tipos, cardinalidad contando el lote, condición) y rechazar con un error que las nombre.

2. Devolver las alertas on_write en BatchReport. check_on_write las pasa a finding_route.route, que solo llega a listeners en proceso (sldb.core, no pública). specIR tiene que releerlas con rules_check(subject), que no se limita a on_write. Pedido: BatchReport.alerts (o findings) con las alertas on_write de cada documento escrito.

3. rules_check(store, 'RelationDoc/<name>') lanza ValueError('sin proyección para RelationDoc:<name>') porque un RelationDoc no es nodo del índice, aunque check_on_write sí evalúa reglas sobre RelationDoc al escribir. Pedido: que rules_check acepte cualquier documento que check_on_write acepte, o que responda con un SLDBDocumentTargetError claro.

4. (Menor) apply_batch/Transaction no dejan nombrar la operación ni la autoridad. La procedencia queda via create_document/save_document_payload, con authority = la del modelo (generated), aunque escriba un agente que, según la decisión IR05 de specIR, escribe 'authored'. Pedido: parámetros opcionales via (etiqueta del llamador) y authority en apply_batch/Transaction, como ya existe actor.
