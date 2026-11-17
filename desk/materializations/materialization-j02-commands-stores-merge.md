---
sldb:
  by: agent
  at: '2026-11-17T00:07:30Z'
  authority: generated
  via: create_document
id: materialization-j02-commands-stores-merge
title: j02 commands stores_merge
source_atoms:
- atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
target_kind: code
target_identity: src/sldb/cli/commands/stores_merge.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_update_fault_tolerance.py
  tests/store/test_merkle_shards.py
tags:
- system:sldb
- topic:store
---

# j02 commands stores_merge

## Intent

materializa en src/sldb/cli/commands/stores_merge.py el atom atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
