---
sldb:
  by: agent
  at: '2026-11-17T00:08:29Z'
  authority: generated
  via: create_document
id: materialization-j02-derived-guard
title: j02 derived_guard
source_atoms:
- atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
target_kind: code
target_identity: src/sldb/store/io/derived_guard.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_update_fault_tolerance.py
  tests/store/test_merkle_shards.py
tags:
- system:sldb
- topic:store
---

# j02 derived_guard

## Intent

materializa en src/sldb/store/io/derived_guard.py el atom atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
