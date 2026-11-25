---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T14:38:05'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# C7: API pública para resolver un store por nombre en el catálogo de la máquina

_Describe the incoming message with enough evidence to triage._

deskops/identity.py mantiene un registro propio de repos por ruta para message send --to y list tasks --include-repos, y falla cuando el nombre no coincide (nota de Governance 20261120-194034). Pedido: API y CLI públicos de sldb para resolver un store o repo por nombre en el catálogo de la máquina (nodo S07). Plan deskops-plugin-de-sldb (deskops/desk/drawer/plans/deskops-plugin-de-sldb, decisión de JP del 25-11: deskops es un plugin sobre sldb, no una reimplementación).
