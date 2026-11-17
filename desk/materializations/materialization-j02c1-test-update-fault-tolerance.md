---
sldb:
  by: agent
  at: '2026-11-17T02:27:23Z'
  authority: generated
  via: create_document
id: materialization-j02c1-test-update-fault-tolerance
title: j02c1 test_update_fault_tolerance
source_atoms:
- atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
target_kind: test
target_identity: tests/store/test_update_fault_tolerance.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_store_seams.py
tags:
- system:sldb
- topic:store
---

# j02c1 test_update_fault_tolerance

## Intent

materializa en tests/store/test_update_fault_tolerance.py el atom atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
