---
sldb:
  by: agent
  at: '2026-11-20T02:57:56Z'
  authority: generated
  via: create_document
id: materialization-cache-ve-reescritura-tests-api-test-select-documents-disk-py
title: caché ve reescritura tests-api-test_select_documents_disk-py
source_atoms:
- atom-las-caches-de-disco-de-sldb-ven-una-reescritura-in-place-de-un-documento-y-stores-build-las-invalida
target_kind: test
target_identity: tests/api/test_select_documents_disk.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_select_documents_disk.py
tags:
- system:sldb
- topic:cache
---

# caché ve reescritura tests-api-test_select_documents_disk-py

## Intent

materializa en tests/api/test_select_documents_disk.py el atom atom-las-caches-de-disco-de-sldb-ven-una-reescritura-in-place-de-un-documento-y-stores-build-las-invalida
