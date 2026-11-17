---
sldb:
  by: agent
  at: '2026-11-17T00:03:15Z'
  authority: generated
  via: create_document
id: materialization-j02-test-update-fault-tolerance
title: j02 test_update_fault_tolerance
source_atoms:
- atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
target_kind: test
target_identity: tests/store/test_update_fault_tolerance.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_update_fault_tolerance.py
  tests/store/test_merkle_shards.py
tags:
- system:sldb
- topic:store
---

# j02 test_update_fault_tolerance

## Intent

materializa en tests/store/test_update_fault_tolerance.py el atom atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
