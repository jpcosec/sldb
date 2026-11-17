---
sldb:
  by: agent
  at: '2026-11-17T12:16:56Z'
  authority: generated
  via: create_document
id: materialization-undo-tools
title: undo tools
source_atoms:
- atom-sldb-mcp-deshace-lotes-con-undo-changes-sobre-una-pila-de-lotes-inversos-por-sesión
target_kind: code
target_identity: src/sldb/mcp/write/tools.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev --extra mcp pytest -q tests/mcp/test_write_tools.py
tags:
- system:sldb
- topic:mcp
---

# undo tools

## Intent

materializa en src/sldb/mcp/write/tools.py el atom atom-sldb-mcp-deshace-lotes-con-undo-changes-sobre-una-pila-de-lotes-inversos-por-sesión
