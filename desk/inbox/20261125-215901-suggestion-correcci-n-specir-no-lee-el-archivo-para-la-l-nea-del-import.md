---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T21:59:01'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Corrección: specIR no lee el archivo para la línea del import

_Describe the incoming message with enough evidence to triage._

Corrige mi nota anterior: specIR no lee código (su test lo prohíbe), así que no usa ast. La línea del import queda desconocida hasta que los hechos de módulo la traigan (attrs.imports_at o similar).
