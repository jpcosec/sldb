---
sldb:
  by: agent
  at: '2026-11-16T14:51:19Z'
  authority: generated
  via: create_document
id: materialization-c1-carga-edge-index
title: c1-carga edge_index
source_atoms:
- atom-cargar-un-store-por-la-api-pública-no-aborta-por-un-documento-inválido-on-invalid-skip-devuelve-los
target_kind: code
target_identity: src/sldb/store/edge_index/edge_index.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
  tests/api/test_api_edges.py tests/test_clean_code_rules.py
tags:
- system:sldb
- topic:store
---

# c1-carga edge_index

## Intent

materializa en src/sldb/store/edge_index/edge_index.py el atom atom-cargar-un-store-por-la-api-pública-no-aborta-por-un-documento-inválido-on-invalid-skip-devuelve-los
