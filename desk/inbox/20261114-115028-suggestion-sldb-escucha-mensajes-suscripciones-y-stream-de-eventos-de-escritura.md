---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-14T11:50:28'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# sldb escucha mensajes: suscripciones y stream de eventos de escritura

_Describe the incoming message with enough evidence to triage._

Idea de JP (2026-11-14): que sldb pueda "estar escuchando" los mensajes.

Hoy un mensaje entre desks (deskops message send) es un archivo en desk/inbox/ trackeado como InboxNoteDoc; nadie reacciona hasta que una sesión lo lee a mano. La idea es que el store avise cuando entra un documento que alguien declaró escuchar.

Forma posible, a discutir:
- Una suscripción declarada en el store (selector sobre modelo/tags, p. ej. InboxNoteDoc con target sldb) y un stream de eventos de escritura (crear/actualizar/borrar con fecha y procedencia), expuesto por la API pública y por sldb serve (SSE o similar).
- Los consumidores (sesiones en herdr, scion, la UI de deskops) se suscriben; sldb no ejecuta agentes, solo emite el evento (sldb = conocimiento, la ejecución es de otros).
- Se cruza con la brecha 9 de IR01 (sldb:20261114-074447-suggestion-specir-brechas-api-p-blica-sldb-para-mcp): el journal fue retirado y no hay consulta de escrituras recientes; un stream de eventos resolvería las dos cosas.

Preguntas al desk: ¿el evento sale de la escritura (Transaction / save_document_payload) o de mirar el árbol (git/inotify), dado que muchos mensajes llegan por git pull de otra máquina? ¿Dónde se declara la suscripción: ViewDoc, RuleDoc con un moment nuevo, o un modelo propio?
