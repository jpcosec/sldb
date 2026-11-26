---
sldb:
  by: agent
  at: '2026-11-26T01:07:02Z'
  authority: generated
  via: create_document
id: materialization-undo-changes-sesiones-docs-architecture-journal-authority-md
title: undo-changes-sesiones docs-architecture-journal-authority-md
source_atoms:
- atom-undo-changes-deshace-un-cambio-aplicado-en-una-sesion-anterior
target_kind: docs
target_identity: docs/architecture/journal-authority.md
validation:
- pytest -q tests/test_mcp_undo_across_sessions.py tests/mcp/test_write_tools.py
tags:
- system:sldb
- topic:undo-changes-sesiones
---

# undo-changes-sesiones docs-architecture-journal-authority-md

## Intent

materializa en docs/architecture/journal-authority.md el atom atom-undo-changes-deshace-un-cambio-aplicado-en-una-sesion-anterior
