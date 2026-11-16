---
sldb:
  by: agent
  at: '2026-11-16T16:19:23Z'
  authority: generated
  via: create_document
id: materialization-c5-mcp-tools
title: c5-mcp tools
source_atoms:
- atom-una-extensión-de-sldb-mcp-agrega-reglas-de-dominio-a-la-escritura-registrando-validadores-de-lote-si
target_kind: code
target_identity: src/sldb/mcp/write/tools.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
tags:
- system:sldb
- topic:clean-code
---

# c5-mcp tools

## Intent

materializa en src/sldb/mcp/write/tools.py el atom atom-una-extensión-de-sldb-mcp-agrega-reglas-de-dominio-a-la-escritura-registrando-validadores-de-lote-si
