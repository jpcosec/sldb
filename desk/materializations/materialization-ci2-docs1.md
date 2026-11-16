---
sldb:
  by: agent
  at: '2026-11-16T22:52:58Z'
  authority: generated
  via: create_document
id: materialization-ci2-docs1
title: ci2 docs1
source_atoms:
- atom-track-con-force-re-indexa-desde-el-archivo-un-documento-ya-trackeado-en-la-misma-ruta
target_kind: code
target_identity: src/sldb/cli/parsers/docs1.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
tags:
- system:sldb
- topic:store
---

# ci2 docs1

## Intent

materializa en src/sldb/cli/parsers/docs1.py el atom atom-track-con-force-re-indexa-desde-el-archivo-un-documento-ya-trackeado-en-la-misma-ruta
