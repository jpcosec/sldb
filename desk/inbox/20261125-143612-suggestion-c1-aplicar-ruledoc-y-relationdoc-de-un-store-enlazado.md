---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T14:36:12'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# C1: aplicar RuleDoc y RelationDoc de un store enlazado

_Describe the incoming message with enough evidence to triage._

Hoy sldb aplica solo las RuleDoc y RelationDoc del store local (docs/architecture/rules.md §3), mientras las ViewDoc ya se leen por enlace (H9). Por eso deskops copia sus reglas de activación y cierre y sus aristas de ciclo de vida a cada desk (deskops/lifecycle.py siembra, desk update copia), y esas copias derivan. Pedido: que las reglas y aristas de un store enlazado (el paquete dueño del modelo) se apliquen en el store que lo enlaza, con la misma resolución que las vistas. Con esto deskops borra la siembra (nodo P02) y las tareas 'advance no derrama reglas' y 'migración a 10 desks'. Plan deskops-plugin-de-sldb (deskops/desk/drawer/plans/deskops-plugin-de-sldb, decisión de JP del 25-11: deskops es un plugin sobre sldb, no una reimplementación).
