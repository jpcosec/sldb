---
sldb:
  by: agent
  at: '2026-11-16T10:53:11Z'
  authority: generated
  via: create_document
id: materialization-mcp-gancho-test-extension
title: mcp-gancho test_extension
source_atoms:
- atom-una-extensión-de-sldb-mcp-agrega-reglas-de-dominio-a-la-escritura-registrando-validadores-de-lote-si
target_kind: test
target_identity: tests/mcp/test_extension.py
validation:
- TMPDIR=/dev/shm uvx --from 'pytest>=8' --with-editable '.[mcp,code]' pytest -q tests/mcp/test_extension.py
  tests/mcp/test_write_tools.py
tags:
- system:sldb
- topic:mcp
---

# mcp-gancho test_extension

## Intent

materializa en tests/mcp/test_extension.py el atom atom-una-extensión-de-sldb-mcp-agrega-reglas-de-dominio-a-la-escritura-registrando-validadores-de-lote-si
