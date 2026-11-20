---
sldb:
  by: agent
  at: '2026-11-20T03:41:04Z'
  authority: generated
  via: create_document
id: materialization-cache-tests-api-test-select-documents-disk-py
title: cache tests-api-test_select_documents_disk-py
source_atoms:
- atom-drop-disk-caches-vive-en-store-disk-caches-py-y-las-dos-caches-de-disco-ven-el-roster-de-cada-modelo
target_kind: test
target_identity: tests/api/test_select_documents_disk.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_select_documents_disk.py
tags:
- system:sldb
- topic:cache
---

# cache tests-api-test_select_documents_disk-py

## Intent

materializa en tests/api/test_select_documents_disk.py el atom atom-drop-disk-caches-vive-en-store-disk-caches-py-y-las-dos-caches-de-disco-ven-el-roster-de-cada-modelo
