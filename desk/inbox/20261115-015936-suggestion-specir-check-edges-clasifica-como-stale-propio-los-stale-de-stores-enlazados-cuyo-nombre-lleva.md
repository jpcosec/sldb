---
sldb:
  by: agent
  at: '2026-11-16T08:20:04Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-15T01:59:36'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:19:48'
---

# [specIR] check_edges clasifica como stale propio los stale de stores enlazados cuyo nombre lleva ':'

_Describe the incoming message with enough evidence to triage._

Detectado en IR03 (task-ir03-servidor-mcp-de-solo-lectura-sobre-un-store-sldb-real) sobre sldb b51e9667 y presente en 6aeba3eb. src/sldb/api/edges/check_edges.py:29 separa linked_stale con s.count(':') == 2. Un documento de un store enlazado cuyo nombre contiene ':' (p. ej. pron:RelationDoc:implements--SurfaceDoc:surface-pron-world-world_template--SpecDoc:spec-01, que llega a IR por deskops) se cuenta como stale propio. En IR, sldb edges check reporta 359 stale propios y EdgeCheckReport.ok da False, mientras --local da Edges OK.

Pedido: clasificar por el store dueño del nodo, no por el conteo de ':'. specIR toma el veredicto con include_linked=False y no reimplementa nada.
