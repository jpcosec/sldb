---
sldb:
  by: agent
  at: '2026-11-17T12:35:45Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-17T09:29:21'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T09:35:22'
---

# Procesos huérfanos de test_second_process_with_the_s… (apply_batch con hold) en /dev/shm

_Describe the incoming message with enough evidence to triage._

Hay 2 procesos huérfanos de una prueba de sldb que siguen vivos en robocop2: python -c ... api.apply_batch ... marks/go, uno lleva 19 h (pytest-607) y el otro 16 h (pytest-652). Son de test_second_process_with_the_s… y esperan un archivo go que nunca llega. No los maté (regla de no pkill). Parece que la prueba no limpia al proceso que retiene si falla o vence su timeout.
