---
sldb:
  by: agent
  at: '2026-11-17T12:17:53Z'
  authority: generated
  via: create_document
id: materialization-undo-test-mutability
title: undo test_mutability
source_atoms:
- atom-sldb-mcp-deshace-lotes-con-undo-changes-sobre-una-pila-de-lotes-inversos-por-sesión
target_kind: test
target_identity: tests/mcp/test_mutability.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev --extra mcp pytest -q tests/mcp/test_write_tools.py
tags:
- system:sldb
- topic:mcp
---

# undo test_mutability

## Intent

materializa en tests/mcp/test_mutability.py el atom atom-sldb-mcp-deshace-lotes-con-undo-changes-sobre-una-pila-de-lotes-inversos-por-sesión
