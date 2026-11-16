---
sldb:
  by: agent
  at: '2026-11-16T23:09:53Z'
  authority: generated
  via: create_document
id: materialization-b2sql-c1-pyproject
title: b2sql-c1 pyproject
source_atoms:
- atom-sldb-code-lee-ddl-de-postgres-y-migraciones-de-sqlmigrate-como-hechos-de-tablas-columnas-vistas-e-ín
target_kind: code
target_identity: pyproject.toml
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
  tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# b2sql-c1 pyproject

## Intent

materializa en pyproject.toml el atom atom-sldb-code-lee-ddl-de-postgres-y-migraciones-de-sqlmigrate-como-hechos-de-tablas-columnas-vistas-e-ín
