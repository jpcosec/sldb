---
sldb:
  by: agent
  at: '2026-11-23T01:42:18Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-20T20:54:49'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-22T22:41:56'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'Convertida en la tarea task-stores-rebuild-index-regenera-desde-su-fuente-los-shards-de-documento-que-git-dejo-con-marcadores-de.
  Sigue en 6ab01b80: rebuild_index.py y el merge driver no cubren core/documents/**.'
---

# Ningún comando de sldb repara un shard de documento .sldb que git dejó en conflicto

_Describe the incoming message with enough evidence to triage._

2026-11-20, IR: al fusionar una rama que tocaba desk/tasks/Board.md, git dejó en conflicto .sldb/core/documents/BoardDoc/Board.yaml (UU) y un shard borrado de un lado y modificado del otro (DU). El merge driver solo cubre store_index.yaml, models/*.yaml y store.yaml. 'sldb stores rebuild-index' falla leyendo el shard con marcadores ('could not find expected :'), y 'sldb docs track --reindex' y 'docs update' también lo leen y fallan. No hay forma por CLI de regenerar un shard de documento desde su .md ni de resolver un DU, y la regla prohíbe tocar .sldb a mano, así que el merge se abortó y el contenido de la rama se aplicó por deskops. Pedido: (1) que rebuild-index (o un comando nuevo, p. ej. 'sldb stores resolve') regenere desde el archivo fuente cada shard de documento con marcadores y quite los de documentos cuyo fuente ya no existe; (2) o que el merge driver cubra también core/documents/**.
