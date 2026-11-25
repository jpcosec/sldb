---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T14:38:40'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# C9: creación de documentos dirigida por el esquema del modelo

_Describe the incoming message with enough evidence to triage._

deskops/cli/model_introspection.py (325 líneas) arma argumentos de CLI desde los campos pydantic de cada modelo para add <tipo>. Pedido (no verificado si sldb docs create ya lo cubre): que sldb cree documentos a partir del esquema del modelo, con flags o YAML, para que deskops no mantenga su propia introspección (nodo P04). Plan deskops-plugin-de-sldb (deskops/desk/drawer/plans/deskops-plugin-de-sldb, decisión de JP del 25-11: deskops es un plugin sobre sldb, no una reimplementación).
