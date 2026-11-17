---
sldb:
  by: agent
  at: '2026-11-17T12:17:24Z'
  authority: generated
  via: create_document
id: materialization-undo-test-extension
title: undo test_extension
source_atoms:
- atom-sldb-mcp-deshace-lotes-con-undo-changes-sobre-una-pila-de-lotes-inversos-por-sesión
target_kind: test
target_identity: tests/mcp/test_extension.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev --extra mcp pytest -q tests/mcp/test_write_tools.py
tags:
- system:sldb
- topic:mcp
---

# undo test_extension

## Intent

materializa en tests/mcp/test_extension.py el atom atom-sldb-mcp-deshace-lotes-con-undo-changes-sobre-una-pila-de-lotes-inversos-por-sesión
