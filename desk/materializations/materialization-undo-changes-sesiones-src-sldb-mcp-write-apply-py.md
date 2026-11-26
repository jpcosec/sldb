---
sldb:
  by: agent
  at: '2026-11-26T01:12:29Z'
  authority: generated
  via: create_document
id: materialization-undo-changes-sesiones-src-sldb-mcp-write-apply-py
title: undo-changes-sesiones src-sldb-mcp-write-apply-py
source_atoms:
- atom-undo-changes-deshace-un-cambio-aplicado-en-una-sesion-anterior
target_kind: code
target_identity: src/sldb/mcp/write/apply.py
validation:
- pytest -q tests/test_mcp_undo_across_sessions.py tests/mcp/test_write_tools.py
tags:
- system:sldb
- topic:undo-changes-sesiones
---

# undo-changes-sesiones src-sldb-mcp-write-apply-py

## Intent

materializa en src/sldb/mcp/write/apply.py el atom atom-undo-changes-deshace-un-cambio-aplicado-en-una-sesion-anterior
