---
sldb:
  by: agent
  at: '2026-11-20T04:32:56Z'
  authority: generated
  via: create_document
id: materialization-move-src-sldb-api-documents-move-document-py
title: move src-sldb-api-documents-move_document-py
source_atoms:
- atom-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-reescribe-en-el-mismo-repo-las-referencias-a-la
target_kind: code
target_identity: src/sldb/api/documents/move_document.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_move_path.py
  tests/cli/test_move_cli.py
tags:
- system:sldb
- topic:cli
---

# move src-sldb-api-documents-move_document-py

## Intent

materializa en src/sldb/api/documents/move_document.py el atom atom-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-reescribe-en-el-mismo-repo-las-referencias-a-la
