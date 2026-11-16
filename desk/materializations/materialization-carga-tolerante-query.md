---
sldb:
  by: agent
  at: '2026-11-16T10:39:22Z'
  authority: generated
  via: create_document
id: materialization-carga-tolerante-query
title: carga-tolerante query
source_atoms:
- atom-cargar-un-store-por-la-api-pública-no-aborta-por-un-documento-inválido-on-invalid-skip-devuelve-los
target_kind: code
target_identity: src/sldb/store/query.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
  tests/api/test_api_edges.py
tags:
- system:sldb
- topic:store
---

# carga-tolerante query

## Intent

materializa en src/sldb/store/query.py el atom atom-cargar-un-store-por-la-api-pública-no-aborta-por-un-documento-inválido-on-invalid-skip-devuelve-los
