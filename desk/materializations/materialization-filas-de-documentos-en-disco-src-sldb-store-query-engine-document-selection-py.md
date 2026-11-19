---
sldb:
  by: agent
  at: '2026-11-19T17:01:55Z'
  authority: generated
  via: create_document
id: materialization-filas-de-documentos-en-disco-src-sldb-store-query-engine-document-selection-py
title: filas de documentos en disco src-sldb-store-query_engine-document_selection-py
source_atoms:
- atom-select-documents-guarda-en-disco-las-filas-de-documentos-para-que-una-vista-no-reparsee-los-shards-e
target_kind: code
target_identity: src/sldb/store/query_engine/document_selection.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_select_documents_disk.py
tags:
- system:sldb
- topic:views
---

# filas de documentos en disco src-sldb-store-query_engine-document_selection-py

## Intent

materializa en src/sldb/store/query_engine/document_selection.py el atom atom-select-documents-guarda-en-disco-las-filas-de-documentos-para-que-una-vista-no-reparsee-los-shards-e
