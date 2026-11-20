---
sldb:
  by: agent
  at: '2026-11-20T04:40:50Z'
  authority: generated
  via: create_document
id: materialization-move-tests-api-test-move-path-py
title: move tests-api-test_move_path-py
source_atoms:
- atom-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-reescribe-en-el-mismo-repo-las-referencias-a-la
target_kind: test
target_identity: tests/api/test_move_path.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_move_path.py
  tests/cli/test_move_cli.py
tags:
- system:sldb
- topic:cli
---

# move tests-api-test_move_path-py

## Intent

materializa en tests/api/test_move_path.py el atom atom-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-reescribe-en-el-mismo-repo-las-referencias-a-la
