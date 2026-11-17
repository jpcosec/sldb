---
sldb:
  by: agent
  at: '2026-11-17T08:10:59Z'
  authority: generated
  via: create_document
id: materialization-k2-pg-test-treesitter-symbols
title: k2-pg test_treesitter_symbols
source_atoms:
- atom-con-el-extra-postgres-las-claves-del-ddl-de-postgres-se-leen-con-el-parser-real-de-postgres-pglast
target_kind: test
target_identity: tests/selfdoc/test_treesitter_symbols.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra postgres --extra dev pytest
  -q tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# k2-pg test_treesitter_symbols

## Intent

materializa en tests/selfdoc/test_treesitter_symbols.py el atom atom-con-el-extra-postgres-las-claves-del-ddl-de-postgres-se-leen-con-el-parser-real-de-postgres-pglast
