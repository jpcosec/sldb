---
sldb:
  by: agent
  at: '2026-11-16T23:17:44Z'
  authority: generated
  via: create_document
id: materialization-b2sql-c1-test-anchors
title: b2sql-c1 test_anchors
source_atoms:
- atom-sldb-code-lee-ddl-de-postgres-y-migraciones-de-sqlmigrate-como-hechos-de-tablas-columnas-vistas-e-ín
target_kind: test
target_identity: tests/api/test_anchors.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
  tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# b2sql-c1 test_anchors

## Intent

materializa en tests/api/test_anchors.py el atom atom-sldb-code-lee-ddl-de-postgres-y-migraciones-de-sqlmigrate-como-hechos-de-tablas-columnas-vistas-e-ín
