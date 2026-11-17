---
sldb:
  by: agent
  at: '2026-11-17T02:26:15Z'
  authority: generated
  via: create_document
id: materialization-j02c1-check-identity
title: j02c1 check_identity
source_atoms:
- atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
target_kind: code
target_identity: tools/check_identity.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_store_seams.py
tags:
- system:sldb
- topic:store
---

# j02c1 check_identity

## Intent

materializa en tools/check_identity.py el atom atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
