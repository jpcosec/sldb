---
sldb:
  by: agent
  at: '2026-11-16T10:41:16Z'
  authority: generated
  via: create_document
id: materialization-carga-tolerante-test-api-edges
title: carga-tolerante test_api_edges
source_atoms:
- atom-cargar-un-store-por-la-api-pública-no-aborta-por-un-documento-inválido-on-invalid-skip-devuelve-los
target_kind: test
target_identity: tests/api/test_api_edges.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
  tests/api/test_api_edges.py
tags:
- system:sldb
- topic:store
---

# carga-tolerante test_api_edges

## Intent

materializa en tests/api/test_api_edges.py el atom atom-cargar-un-store-por-la-api-pública-no-aborta-por-un-documento-inválido-on-invalid-skip-devuelve-los
