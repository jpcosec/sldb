---
sldb:
  by: agent
  at: '2026-11-21T12:15:35Z'
  authority: generated
  via: create_document
id: materialization-store-src-sldb-store-documents-dirty-py
title: store src-sldb-store-documents_dirty-py
source_atoms:
- atom-el-conjunto-de-documentos-sucios-se-persiste-en-sldb
target_kind: code
target_identity: src/sldb/store/documents_dirty.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests
tags:
- system:sldb
- topic:store
---

# store src-sldb-store-documents_dirty-py

## Intent

materializa en src/sldb/store/documents_dirty.py el atom atom-el-conjunto-de-documentos-sucios-se-persiste-en-sldb
