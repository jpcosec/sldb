---
sldb:
  by: agent
  at: '2026-11-16T23:20:44Z'
  authority: generated
  via: create_document
id: materialization-b2sql-c1-django-0001-initial
title: b2sql-c1 django 0001_initial
source_atoms:
- atom-sldb-code-lee-ddl-de-postgres-y-migraciones-de-sqlmigrate-como-hechos-de-tablas-columnas-vistas-e-ín
target_kind: test
target_identity: tests/fixtures/treesitter/sql/django/0001_initial.sql
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
  tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# b2sql-c1 django 0001_initial

## Intent

materializa en tests/fixtures/treesitter/sql/django/0001_initial.sql el atom atom-sldb-code-lee-ddl-de-postgres-y-migraciones-de-sqlmigrate-como-hechos-de-tablas-columnas-vistas-e-ín
