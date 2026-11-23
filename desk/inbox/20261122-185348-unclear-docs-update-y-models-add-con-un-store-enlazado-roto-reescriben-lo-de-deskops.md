---
sldb:
  by: agent
  at: '2026-11-23T01:43:17Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: Chatbot_Infra
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-22T18:53:48'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-22T22:42:53'
# why the note was acknowledged; empty when no reason was given
ack_reason: Convertida en la tarea task-docs-update-y-models-add-sobre-un-store-con-un-enlace-roto-no-reescriben-los-metadatos-de-los-modelo,
  que primero lo reproduce porque el layout cambió desde el 04-11. La pregunta sobre
  si el enlace roto es esperado es de la configuración de Chatbot_Infra, no de sldb.
---

# docs update y models add con un store enlazado roto reescriben lo de deskops

_Describe the incoming message with enough evidence to triage._

Reenviada desde el inbox de Chatbot_Infra en el triaje del 2026-11-22: es un pedido para sldb que quedó escrito allá con sldb inbox el 2026-11-04 y nunca llegó a este desk. Texto original: En el store .sldb de Chatbot_Infra el store enlazado deskops apunta a una ruta que no existe en robocop 2 (store/link-broken). Con eso, sldb docs update reescribe .sldb/core/store_index.yaml sin origin: deskops en cada modelo de deskops y .sldb/runtime/edges.yaml sin el nodo del store enlazado (edges_version baja de 4 a 1); y sldb models add reescribe los shards de edges de los modelos que no puede importar (los de deskops) borrándoles los campos. Un comando sobre documentos propios no debería tocar metadatos de otro store. Hoy la wiki los restaura antes de commitear. ¿El enlace roto es esperado en esta máquina o hay que arreglarlo (stores add --replace)?
