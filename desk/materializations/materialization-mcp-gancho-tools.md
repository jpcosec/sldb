---
sldb:
  by: agent
  at: '2026-11-16T10:52:48Z'
  authority: generated
  via: create_document
id: materialization-mcp-gancho-tools
title: mcp-gancho tools
source_atoms:
- atom-una-extensión-de-sldb-mcp-agrega-reglas-de-dominio-a-la-escritura-registrando-validadores-de-lote-si
target_kind: code
target_identity: src/sldb/mcp/write/tools.py
validation:
- TMPDIR=/dev/shm uvx --from 'pytest>=8' --with-editable '.[mcp,code]' pytest -q tests/mcp/test_extension.py
  tests/mcp/test_write_tools.py
tags:
- system:sldb
- topic:mcp
---

# mcp-gancho tools

## Intent

materializa en src/sldb/mcp/write/tools.py el atom atom-una-extensión-de-sldb-mcp-agrega-reglas-de-dominio-a-la-escritura-registrando-validadores-de-lote-si
