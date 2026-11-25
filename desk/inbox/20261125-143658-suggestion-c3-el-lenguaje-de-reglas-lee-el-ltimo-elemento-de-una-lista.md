---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T14:36:58'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# C3: el lenguaje de reglas lee el último elemento de una lista

_Describe the incoming message with enough evidence to triage._

deskops/models/task_lifecycle.py valida en pydantic que status, current_node y el último elemento de history sean coherentes con la arista que llegó a current_node, y lee el grafo del paquete, no el del desk. Pedido (no verificado si ya existe): que una regla on_write pueda leer el último elemento de un campo lista y compararlo con la arista entrante, para que esa coherencia sea una RuleDoc (nodo W06). Plan deskops-plugin-de-sldb (deskops/desk/drawer/plans/deskops-plugin-de-sldb, decisión de JP del 25-11: deskops es un plugin sobre sldb, no una reimplementación).
