---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: minegocio
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-22T23:34:51'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# sldb serve: /document* y /save no resuelven Tipo/nombre (homónimos entre modelos)

_Describe the incoming message with enough evidence to triage._

sldb serve no admite Tipo/nombre en /document, /document/ir, /document/segments (tracked_docs.is_tracked compara doc.name exacto: 404 Unknown doc) ni en POST /save update/delete (save_routes indexa current por doc.name y batch_prevalidate._existing/find_doc toman el primer modelo con ese nombre: 409). Con dos documentos homónimos en modelos distintos ninguno se puede abrir ni guardar por serve; /render, /extract, /sections y /fields sí aceptan Tipo/nombre. Detalle y reproducción en minegocio tests/test_wiki_servida.py (prueba xfail test_dos_paginas_con_el_mismo_nombre_se_abren_y_se_guardan_cada_una). Además sería más firme que el 422 de /save devolviera exc.errors() como details (como /extract/segments) en vez de solo el str del ValidationError.
