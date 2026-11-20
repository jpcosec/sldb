---
sldb:
  by: agent
  at: '2026-11-20T04:31:49Z'
  authority: generated
  via: create_document
id: materialization-move-knowledge-surfaces-surface-sldb-move-md
title: move knowledge-surfaces-surface-sldb-move-md
source_atoms:
- atom-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-reescribe-en-el-mismo-repo-las-referencias-a-la
target_kind: docs
target_identity: knowledge/surfaces/surface-sldb-move.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_move_path.py
  tests/cli/test_move_cli.py
tags:
- system:sldb
- topic:cli
---

# move knowledge-surfaces-surface-sldb-move-md

## Intent

materializa en knowledge/surfaces/surface-sldb-move.md el atom atom-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-reescribe-en-el-mismo-repo-las-referencias-a-la
