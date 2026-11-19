---
sldb:
  by: agent
  at: '2026-11-19T17:02:52Z'
  authority: generated
  via: create_document
id: materialization-filas-de-documentos-en-disco-tests-api-test-select-documents-disk-py
title: filas de documentos en disco tests-api-test_select_documents_disk-py
source_atoms:
- atom-select-documents-guarda-en-disco-las-filas-de-documentos-para-que-una-vista-no-reparsee-los-shards-e
target_kind: test
target_identity: tests/api/test_select_documents_disk.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_select_documents_disk.py
tags:
- system:sldb
- topic:views
---

# filas de documentos en disco tests-api-test_select_documents_disk-py

## Intent

materializa en tests/api/test_select_documents_disk.py el atom atom-select-documents-guarda-en-disco-las-filas-de-documentos-para-que-una-vista-no-reparsee-los-shards-e
