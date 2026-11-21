---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: repo-governance
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-20T19:43:04'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# Versionar sldb y fijarlo en quienes lo usan

_Describe the incoming message with enough evidence to triage._

Del diagnóstico de Governance: sldb no tiene versiones publicadas al día (pyproject dice 0.1.13 sin tag) y cada repo lo instala desde un commit distinto (robocop-ci lo usa en 9f1412ad). Pedido: tags cuando un cambio rompe compatibilidad y CI de main en verde, para que los repos fijen versión en pulse.yml, ci.yml y tests/versions.txt. Reemplaza, en lo que toca a sldb, la tarea de Governance «versionar sldb, deskops y spec2viz».
