---
sldb:
  by: agent
  at: '2026-11-16T23:58:53Z'
  authority: generated
  via: create_document
id: materialization-j02-versionado-y-colaboracion
title: j02 versionado-y-colaboracion
source_atoms:
- atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
target_kind: doc
target_identity: docs/versionado-y-colaboracion.md
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_update_fault_tolerance.py
  tests/store/test_merkle_shards.py
tags:
- system:sldb
- topic:store
---

# j02 versionado-y-colaboracion

## Intent

materializa en docs/versionado-y-colaboracion.md el atom atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
