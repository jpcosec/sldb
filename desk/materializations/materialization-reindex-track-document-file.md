---
sldb:
  by: agent
  at: '2026-11-19T10:59:09Z'
  authority: generated
  via: create_document
id: materialization-reindex-track-document-file
title: reindex track_document_file
source_atoms:
- atom-docs-track-reindex-re-indexa-un-documento-trackeado-validandolo-a-diferencia-de-force
target_kind: code
target_identity: src/sldb/api/documents/track_document_file.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_api_documents.py
tags:
- system:sldb
- topic:cli
---

# reindex track_document_file

## Intent

materializa en src/sldb/api/documents/track_document_file.py el atom atom-docs-track-reindex-re-indexa-un-documento-trackeado-validandolo-a-diferencia-de-force
