---
sldb:
  by: agent
  at: '2026-11-11T08:55:48Z'
  authority: generated
  via: create_document
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-11T11:00:00'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# H9: run_view no encuentra una ViewDoc de un store enlazado ('Unknown view'); bloquea CC34 de deskops (DA4)

_Describe the incoming message with enough evidence to triage._

Hallado por CC34 de deskops (worker cc34, 2026-11-11), probado con sldb 1c3132aa. Un store que enlaza a otro store que trackea la ViewDoc da 'Unknown view' en run_view, y por lo tanto en sldb serve GET /views/<x>. Dos causas: (1) el índice compuesto nombra el nodo enlazado '<link>:ViewDoc:<name>' (por ejemplo 'lib:ViewDoc:board') y load_view busca 'ViewDoc:<name>'; (2) read_view resuelve semantics.path contra el project_root local, no contra el root del store enlazado. Consecuencia: la decisión DA4 de deskops (ViewDoc solo como semillas del paquete, sin desk/views/, encontradas por el store de deskops enlazado) no funciona en ningún desk que no sea el propio repo deskops. Esperado: load_view resuelve una ViewDoc de un store enlazado (prueba '<link>:ViewDoc:<name>' cuando no hay local, o por nombre calificado) y lee su archivo desde el root del store que la trackea. Test: un store A que enlaza a B con la ViewDoc en B; run_view(A, 'board') la encuentra y la evalúa sobre los documentos de A.
