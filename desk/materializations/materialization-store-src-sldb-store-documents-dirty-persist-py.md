---
sldb:
  by: agent
  at: '2026-11-21T12:16:04Z'
  authority: generated
  via: create_document
id: materialization-store-src-sldb-store-documents-dirty-persist-py
title: store src-sldb-store-documents_dirty_persist-py
source_atoms:
- atom-el-conjunto-de-documentos-sucios-se-persiste-en-sldb
target_kind: code
target_identity: src/sldb/store/documents_dirty_persist.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests
tags:
- system:sldb
- topic:store
---

# store src-sldb-store-documents_dirty_persist-py

## Intent

materializa en src/sldb/store/documents_dirty_persist.py el atom atom-el-conjunto-de-documentos-sucios-se-persiste-en-sldb
