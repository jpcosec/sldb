---
sldb:
  by: agent
  at: '2026-11-20T04:40:16Z'
  authority: generated
  via: create_document
id: materialization-move-src-sldb-cli-parsers-project-py
title: move src-sldb-cli-parsers-project-py
source_atoms:
- atom-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-reescribe-en-el-mismo-repo-las-referencias-a-la
target_kind: code
target_identity: src/sldb/cli/parsers/project.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_move_path.py
  tests/cli/test_move_cli.py
tags:
- system:sldb
- topic:cli
---

# move src-sldb-cli-parsers-project-py

## Intent

materializa en src/sldb/cli/parsers/project.py el atom atom-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-reescribe-en-el-mismo-repo-las-referencias-a-la
