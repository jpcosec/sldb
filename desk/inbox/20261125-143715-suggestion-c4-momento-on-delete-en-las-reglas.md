---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T14:37:15'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# C4: momento on_delete en las reglas

_Describe the incoming message with enough evidence to triage._

Al cerrar, deskops borra el archivo de la tarea aunque otras tareas la citen en inherits_from, y las herederas dejan de cargar. Pedido: un momento on_delete en RuleDoc, o que borrar/destrackear rechace un documento con referrers que dependen de él según una regla del modelo. Plan deskops-plugin-de-sldb (deskops/desk/drawer/plans/deskops-plugin-de-sldb, decisión de JP del 25-11: deskops es un plugin sobre sldb, no una reimplementación).
