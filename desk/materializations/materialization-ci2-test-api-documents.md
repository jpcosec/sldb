---
sldb:
  by: agent
  at: '2026-11-16T22:53:38Z'
  authority: generated
  via: create_document
id: materialization-ci2-test-api-documents
title: ci2 test_api_documents
source_atoms:
- atom-track-con-force-re-indexa-desde-el-archivo-un-documento-ya-trackeado-en-la-misma-ruta
target_kind: test
target_identity: tests/api/test_api_documents.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
tags:
- system:sldb
- topic:store
---

# ci2 test_api_documents

## Intent

materializa en tests/api/test_api_documents.py el atom atom-track-con-force-re-indexa-desde-el-archivo-un-documento-ya-trackeado-en-la-misma-ruta
