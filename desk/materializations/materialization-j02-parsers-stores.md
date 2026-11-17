---
sldb:
  by: agent
  at: '2026-11-17T00:01:18Z'
  authority: generated
  via: create_document
id: materialization-j02-parsers-stores
title: j02 parsers stores
source_atoms:
- atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
target_kind: code
target_identity: src/sldb/cli/parsers/stores.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_update_fault_tolerance.py
  tests/store/test_merkle_shards.py
tags:
- system:sldb
- topic:store
---

# j02 parsers stores

## Intent

materializa en src/sldb/cli/parsers/stores.py el atom atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
