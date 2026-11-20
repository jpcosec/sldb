---
sldb:
  by: agent
  at: '2026-11-20T04:30:44Z'
  authority: generated
  via: create_document
id: materialization-move-docs-architecture-transactions-md
title: move docs-architecture-transactions-md
source_atoms:
- atom-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-reescribe-en-el-mismo-repo-las-referencias-a-la
target_kind: docs
target_identity: docs/architecture/transactions.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_move_path.py
  tests/cli/test_move_cli.py
tags:
- system:sldb
- topic:cli
---

# move docs-architecture-transactions-md

## Intent

materializa en docs/architecture/transactions.md el atom atom-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-reescribe-en-el-mismo-repo-las-referencias-a-la
