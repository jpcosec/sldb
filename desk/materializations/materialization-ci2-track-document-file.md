---
sldb:
  by: agent
  at: '2026-11-16T22:52:11Z'
  authority: generated
  via: create_document
id: materialization-ci2-track-document-file
title: ci2 track_document_file
source_atoms:
- atom-track-con-force-re-indexa-desde-el-archivo-un-documento-ya-trackeado-en-la-misma-ruta
target_kind: code
target_identity: src/sldb/api/documents/track_document_file.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
tags:
- system:sldb
- topic:store
---

# ci2 track_document_file

## Intent

materializa en src/sldb/api/documents/track_document_file.py el atom atom-track-con-force-re-indexa-desde-el-archivo-un-documento-ya-trackeado-en-la-misma-ruta
