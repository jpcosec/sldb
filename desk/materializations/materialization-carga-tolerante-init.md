---
sldb:
  by: agent
  at: '2026-11-16T10:40:08Z'
  authority: generated
  via: create_document
id: materialization-carga-tolerante-init
title: carga-tolerante __init__
source_atoms:
- atom-cargar-un-store-por-la-api-pública-no-aborta-por-un-documento-inválido-on-invalid-skip-devuelve-los
target_kind: code
target_identity: src/sldb/api/__init__.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
  tests/api/test_api_edges.py
tags:
- system:sldb
- topic:store
---

# carga-tolerante __init__

## Intent

materializa en src/sldb/api/__init__.py el atom atom-cargar-un-store-por-la-api-pública-no-aborta-por-un-documento-inválido-on-invalid-skip-devuelve-los
