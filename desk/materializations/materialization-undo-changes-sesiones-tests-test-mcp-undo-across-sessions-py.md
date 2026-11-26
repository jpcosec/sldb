---
sldb:
  by: agent
  at: '2026-11-26T01:14:40Z'
  authority: generated
  via: create_document
id: materialization-undo-changes-sesiones-tests-test-mcp-undo-across-sessions-py
title: undo-changes-sesiones tests-test_mcp_undo_across_sessions-py
source_atoms:
- atom-undo-changes-deshace-un-cambio-aplicado-en-una-sesion-anterior
target_kind: test
target_identity: tests/test_mcp_undo_across_sessions.py
validation:
- pytest -q tests/test_mcp_undo_across_sessions.py tests/mcp/test_write_tools.py
tags:
- system:sldb
- topic:undo-changes-sesiones
---

# undo-changes-sesiones tests-test_mcp_undo_across_sessions-py

## Intent

materializa en tests/test_mcp_undo_across_sessions.py el atom atom-undo-changes-deshace-un-cambio-aplicado-en-una-sesion-anterior
