---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T14:38:22'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# C8: chequeo 'el store corresponde al árbol' para pre-commit y CI

_Describe the incoming message with enough evidence to triage._

Los desks commitean archivos de desk/ sin que el store .sldb/core corresponda, y se descubre tarde (nota de Governance 20261121-040315). Pedido: un chequeo de sldb apto para pre-commit y CI que falle si el store no corresponde al árbol versionado, con un instalador del hook. Relacionado con la decisión de sldb sobre el hook de Write/Edit. Plan deskops-plugin-de-sldb (deskops/desk/drawer/plans/deskops-plugin-de-sldb, decisión de JP del 25-11: deskops es un plugin sobre sldb, no una reimplementación).
