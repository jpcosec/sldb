---
sldb:
  by: agent
  at: '2026-11-17T00:06:02Z'
  authority: generated
  via: create_document
id: materialization-j02-merge-driver-install
title: j02 merge_driver_install
source_atoms:
- atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
target_kind: code
target_identity: src/sldb/api/stores/merge_driver_install.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_update_fault_tolerance.py
  tests/store/test_merkle_shards.py
tags:
- system:sldb
- topic:store
---

# j02 merge_driver_install

## Intent

materializa en src/sldb/api/stores/merge_driver_install.py el atom atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
