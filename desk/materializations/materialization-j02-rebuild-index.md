---
sldb:
  by: agent
  at: '2026-11-17T00:06:34Z'
  authority: generated
  via: create_document
id: materialization-j02-rebuild-index
title: j02 rebuild_index
source_atoms:
- atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
target_kind: code
target_identity: src/sldb/api/stores/rebuild_index.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_update_fault_tolerance.py
  tests/store/test_merkle_shards.py
tags:
- system:sldb
- topic:store
---

# j02 rebuild_index

## Intent

materializa en src/sldb/api/stores/rebuild_index.py el atom atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
