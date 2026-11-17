---
sldb:
  by: agent
  at: '2026-11-17T08:09:44Z'
  authority: generated
  via: create_document
id: materialization-k2-pg-sql-pg-keys
title: k2-pg sql_pg_keys
source_atoms:
- atom-con-el-extra-postgres-las-claves-del-ddl-de-postgres-se-leen-con-el-parser-real-de-postgres-pglast
target_kind: code
target_identity: src/sldb/code/sql_pg_keys.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra postgres --extra dev pytest
  -q tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# k2-pg sql_pg_keys

## Intent

materializa en src/sldb/code/sql_pg_keys.py el atom atom-con-el-extra-postgres-las-claves-del-ddl-de-postgres-se-leen-con-el-parser-real-de-postgres-pglast
