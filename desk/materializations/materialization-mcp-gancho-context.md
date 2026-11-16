---
sldb:
  by: agent
  at: '2026-11-16T10:51:40Z'
  authority: generated
  via: create_document
id: materialization-mcp-gancho-context
title: mcp-gancho context
source_atoms:
- atom-una-extensión-de-sldb-mcp-agrega-reglas-de-dominio-a-la-escritura-registrando-validadores-de-lote-si
target_kind: code
target_identity: src/sldb/mcp/context.py
validation:
- TMPDIR=/dev/shm uvx --from 'pytest>=8' --with-editable '.[mcp,code]' pytest -q tests/mcp/test_extension.py
  tests/mcp/test_write_tools.py
tags:
- system:sldb
- topic:mcp
---

# mcp-gancho context

## Intent

materializa en src/sldb/mcp/context.py el atom atom-una-extensión-de-sldb-mcp-agrega-reglas-de-dominio-a-la-escritura-registrando-validadores-de-lote-si
