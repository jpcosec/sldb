---
sldb:
  by: agent
  at: '2026-11-17T12:13:21Z'
  authority: generated
  via: create_document
id: materialization-undo-registry
title: undo registry
source_atoms:
- atom-sldb-mcp-deshace-lotes-con-undo-changes-sobre-una-pila-de-lotes-inversos-por-sesión
target_kind: code
target_identity: src/sldb/mcp/registry.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev --extra mcp pytest -q tests/mcp/test_write_tools.py
tags:
- system:sldb
- topic:mcp
---

# undo registry

## Intent

materializa en src/sldb/mcp/registry.py el atom atom-sldb-mcp-deshace-lotes-con-undo-changes-sobre-una-pila-de-lotes-inversos-por-sesión
