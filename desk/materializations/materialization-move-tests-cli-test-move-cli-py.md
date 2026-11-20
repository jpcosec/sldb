---
sldb:
  by: agent
  at: '2026-11-20T04:42:23Z'
  authority: generated
  via: create_document
id: materialization-move-tests-cli-test-move-cli-py
title: move tests-cli-test_move_cli-py
source_atoms:
- atom-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-reescribe-en-el-mismo-repo-las-referencias-a-la
target_kind: test
target_identity: tests/cli/test_move_cli.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_move_path.py
  tests/cli/test_move_cli.py
tags:
- system:sldb
- topic:cli
---

# move tests-cli-test_move_cli-py

## Intent

materializa en tests/cli/test_move_cli.py el atom atom-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-reescribe-en-el-mismo-repo-las-referencias-a-la
