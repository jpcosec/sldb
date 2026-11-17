---
sldb:
  by: agent
  at: '2026-11-17T00:15:04Z'
  authority: generated
  via: create_document
id: materialization-j02-update-store-indexes
title: j02 update_store_indexes
source_atoms:
- atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
target_kind: code
target_identity: src/sldb/api/stores/update_store_indexes.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_merkle_shards.py
tags:
- system:sldb
- topic:store
---

# j02 update_store_indexes

## Intent

materializa en src/sldb/api/stores/update_store_indexes.py el atom atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r (rebuild-index reutiliza la recomputación de índices, sin cambiarla)
