---
sldb:
  by: agent
  at: '2026-11-26T01:10:50Z'
  authority: generated
  via: create_document
id: materialization-undo-changes-sesiones-src-sldb-api-documents-undo-batches-py
title: undo-changes-sesiones src-sldb-api-documents-undo_batches-py
source_atoms:
- atom-undo-changes-deshace-un-cambio-aplicado-en-una-sesion-anterior
target_kind: code
target_identity: src/sldb/api/documents/undo_batches.py
validation:
- pytest -q tests/test_mcp_undo_across_sessions.py tests/mcp/test_write_tools.py
tags:
- system:sldb
- topic:undo-changes-sesiones
---

# undo-changes-sesiones src-sldb-api-documents-undo_batches-py

## Intent

materializa en src/sldb/api/documents/undo_batches.py el atom atom-undo-changes-deshace-un-cambio-aplicado-en-una-sesion-anterior
