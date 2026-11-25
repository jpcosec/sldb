---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T14:37:31'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# C5: punto de extensión del CLI de sldb para los verbos de un plugin

_Describe the incoming message with enough evidence to triage._

sldb mcp ya acepta --extension (docs/architecture/mcp.md). Pedido: un punto equivalente para el CLI, para que un plugin como deskops registre sus verbos de workflow (advance, closeout, dispatch, review) sobre sldb en vez de mantener un CLI paralelo de 108 comandos (deskops/cli/registry.py, 2151 líneas), donde el CRUD repite sldb docs create/list/show y fields update. Plan deskops-plugin-de-sldb (deskops/desk/drawer/plans/deskops-plugin-de-sldb, decisión de JP del 25-11: deskops es un plugin sobre sldb, no una reimplementación).
