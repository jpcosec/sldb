---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T14:37:48'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# C6: chequeo y arreglo de rutas absolutas en campos de referencia

_Describe the incoming message with enough evidence to triage._

deskops/absolute_paths.py (326 líneas) detecta y reescribe rutas absolutas de máquina en campos de referencia de documentos y las resuelve por el registro de repos. Es genérico: pedido de que sldb lo chequee (stores check) y lo arregle resolviendo por el nombre del store en el catálogo (nodo P04). Plan deskops-plugin-de-sldb (deskops/desk/drawer/plans/deskops-plugin-de-sldb, decisión de JP del 25-11: deskops es un plugin sobre sldb, no una reimplementación).
