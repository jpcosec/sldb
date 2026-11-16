---
sldb:
  by: agent
  at: '2026-11-16T10:40:54Z'
  authority: generated
  via: create_document
id: materialization-carga-tolerante-test-api-documents
title: carga-tolerante test_api_documents
source_atoms:
- atom-cargar-un-store-por-la-api-pública-no-aborta-por-un-documento-inválido-on-invalid-skip-devuelve-los
target_kind: test
target_identity: tests/api/test_api_documents.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
  tests/api/test_api_edges.py
tags:
- system:sldb
- topic:store
---

# carga-tolerante test_api_documents

## Intent

materializa en tests/api/test_api_documents.py el atom atom-cargar-un-store-por-la-api-pública-no-aborta-por-un-documento-inválido-on-invalid-skip-devuelve-los
