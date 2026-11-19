---
sldb:
  by: agent
  at: '2026-11-19T11:00:34Z'
  authority: generated
  via: create_document
id: materialization-reindex-test-api-documents
title: reindex test_api_documents
source_atoms:
- atom-docs-track-reindex-re-indexa-un-documento-trackeado-validandolo-a-diferencia-de-force
target_kind: test
target_identity: tests/api/test_api_documents.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_api_documents.py
tags:
- system:sldb
- topic:cli
---

# reindex test_api_documents

## Intent

materializa en tests/api/test_api_documents.py el atom atom-docs-track-reindex-re-indexa-un-documento-trackeado-validandolo-a-diferencia-de-force
