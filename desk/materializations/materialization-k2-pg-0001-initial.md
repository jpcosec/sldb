---
sldb:
  by: agent
  at: '2026-11-17T08:11:23Z'
  authority: generated
  via: create_document
id: materialization-k2-pg-0001-initial
title: k2-pg 0001_initial
source_atoms:
- atom-con-el-extra-postgres-las-claves-del-ddl-de-postgres-se-leen-con-el-parser-real-de-postgres-pglast
target_kind: test
target_identity: tests/fixtures/treesitter/sql/django/0001_initial.sql
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra postgres --extra dev pytest
  -q tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# k2-pg 0001_initial

## Intent

materializa en tests/fixtures/treesitter/sql/django/0001_initial.sql el atom atom-con-el-extra-postgres-las-claves-del-ddl-de-postgres-se-leen-con-el-parser-real-de-postgres-pglast
