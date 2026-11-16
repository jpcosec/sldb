---
sldb:
  by: agent
  at: '2026-11-16T10:53:56Z'
  authority: generated
  via: create_document
id: materialization-mcp-gancho-mcp
title: mcp-gancho mcp
source_atoms:
- atom-una-extensión-de-sldb-mcp-agrega-reglas-de-dominio-a-la-escritura-registrando-validadores-de-lote-si
target_kind: doc
target_identity: docs/architecture/mcp.md
validation:
- TMPDIR=/dev/shm uvx --from 'pytest>=8' --with-editable '.[mcp,code]' pytest -q tests/mcp/test_extension.py
  tests/mcp/test_write_tools.py
tags:
- system:sldb
- topic:mcp
---

# mcp-gancho mcp

## Intent

materializa en docs/architecture/mcp.md el atom atom-una-extensión-de-sldb-mcp-agrega-reglas-de-dominio-a-la-escritura-registrando-validadores-de-lote-si
