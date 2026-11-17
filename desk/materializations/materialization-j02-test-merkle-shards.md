---
sldb:
  by: agent
  at: '2026-11-17T00:02:45Z'
  authority: generated
  via: create_document
id: materialization-j02-test-merkle-shards
title: j02 test_merkle_shards
source_atoms:
- atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
target_kind: test
target_identity: tests/store/test_merkle_shards.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_update_fault_tolerance.py
  tests/store/test_merkle_shards.py
tags:
- system:sldb
- topic:store
---

# j02 test_merkle_shards

## Intent

materializa en tests/store/test_merkle_shards.py el atom atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
