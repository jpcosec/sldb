---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-27T14:11:35'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# sldb no tiene comando para declarar un espacio de nombres de etiquetas

_Describe the incoming message with enough evidence to triage._

Viene de mepu (27-11): al etiquetar tareas con «reunion:teva-2026-11-27», deskops edit task falló con SLDBRuleViolationError rules/builtin:tag_namespace:reunion porque el espacio de nombres no estaba declarado. sldb tags solo trae namespaces (listar), tree y check: no hay forma de declarar uno nuevo por CLI, así que hubo que agregarlo a mano en tag_namespaces de .sldb/store.yaml (name, hierarchical, folder_axis). Pedido: un comando del estilo «sldb tags namespaces add <nombre> [--hierarchical] [--folder-axis] [--anchored-by ...] --store <store>», y que el error de builtin:tag_namespace sugiera ese comando junto a la lista de los declarados.
