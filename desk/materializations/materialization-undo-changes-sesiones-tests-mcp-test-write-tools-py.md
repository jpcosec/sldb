---
sldb:
  by: agent
  at: '2026-11-26T01:14:07Z'
  authority: generated
  via: create_document
id: materialization-undo-changes-sesiones-tests-mcp-test-write-tools-py
title: undo-changes-sesiones tests-mcp-test_write_tools-py
source_atoms:
- atom-undo-changes-deshace-un-cambio-aplicado-en-una-sesion-anterior
target_kind: test
target_identity: tests/mcp/test_write_tools.py
validation:
- pytest -q tests/test_mcp_undo_across_sessions.py tests/mcp/test_write_tools.py
tags:
- system:sldb
- topic:undo-changes-sesiones
---

# undo-changes-sesiones tests-mcp-test_write_tools-py

## Intent

materializa en tests/mcp/test_write_tools.py el atom atom-undo-changes-deshace-un-cambio-aplicado-en-una-sesion-anterior
