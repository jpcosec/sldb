---
sldb:
  by: agent
  at: '2026-11-20T04:41:22Z'
  authority: generated
  via: create_document
id: materialization-move-tests-cli-init-py
title: move tests-cli-__init__-py
source_atoms:
- atom-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-reescribe-en-el-mismo-repo-las-referencias-a-la
target_kind: test
target_identity: tests/cli/__init__.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_move_path.py
  tests/cli/test_move_cli.py
tags:
- system:sldb
- topic:cli
---

# move tests-cli-__init__-py

## Intent

materializa en tests/cli/__init__.py el atom atom-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-reescribe-en-el-mismo-repo-las-referencias-a-la
