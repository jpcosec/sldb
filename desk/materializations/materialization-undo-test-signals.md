---
sldb:
  by: agent
  at: '2026-11-17T12:18:25Z'
  authority: generated
  via: create_document
id: materialization-undo-test-signals
title: undo test_signals
source_atoms:
- atom-sldb-mcp-deshace-lotes-con-undo-changes-sobre-una-pila-de-lotes-inversos-por-sesión
target_kind: test
target_identity: tests/mcp/test_signals.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev --extra mcp pytest -q tests/mcp/test_write_tools.py
tags:
- system:sldb
- topic:mcp
---

# undo test_signals

## Intent

materializa en tests/mcp/test_signals.py el atom atom-sldb-mcp-deshace-lotes-con-undo-changes-sobre-una-pila-de-lotes-inversos-por-sesión
