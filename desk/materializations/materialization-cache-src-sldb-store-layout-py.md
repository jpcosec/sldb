---
sldb:
  by: agent
  at: '2026-11-20T03:40:34Z'
  authority: generated
  via: create_document
id: materialization-cache-src-sldb-store-layout-py
title: cache src-sldb-store-layout-py
source_atoms:
- atom-drop-disk-caches-vive-en-store-disk-caches-py-y-las-dos-caches-de-disco-ven-el-roster-de-cada-modelo
target_kind: code
target_identity: src/sldb/store/layout.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_select_documents_disk.py
tags:
- system:sldb
- topic:cache
---

# cache src-sldb-store-layout-py

## Intent

materializa en src/sldb/store/layout.py el atom atom-drop-disk-caches-vive-en-store-disk-caches-py-y-las-dos-caches-de-disco-ven-el-roster-de-cada-modelo
