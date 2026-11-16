---
sldb:
  by: agent
  at: '2026-11-16T10:39:45Z'
  authority: generated
  via: create_document
id: materialization-carga-tolerante-runtime-documents
title: carga-tolerante runtime_documents
source_atoms:
- atom-cargar-un-store-por-la-api-pública-no-aborta-por-un-documento-inválido-on-invalid-skip-devuelve-los
target_kind: code
target_identity: src/sldb/api/documents/runtime_documents.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
  tests/api/test_api_edges.py
tags:
- system:sldb
- topic:store
---

# carga-tolerante runtime_documents

## Intent

materializa en src/sldb/api/documents/runtime_documents.py el atom atom-cargar-un-store-por-la-api-pública-no-aborta-por-un-documento-inválido-on-invalid-skip-devuelve-los
