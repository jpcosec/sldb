---
sldb:
  by: agent
  at: '2026-11-16T22:51:31Z'
  authority: generated
  via: create_document
id: materialization-ci2-ops
title: ci2 ops
source_atoms:
- atom-track-con-force-re-indexa-desde-el-archivo-un-documento-ya-trackeado-en-la-misma-ruta
target_kind: code
target_identity: src/sldb/store/ops.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
tags:
- system:sldb
- topic:store
---

# ci2 ops

## Intent

materializa en src/sldb/store/ops.py el atom atom-track-con-force-re-indexa-desde-el-archivo-un-documento-ya-trackeado-en-la-misma-ruta
