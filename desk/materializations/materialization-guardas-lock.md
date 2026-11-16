---
sldb:
  by: agent
  at: '2026-11-16T19:46:19Z'
  authority: generated
  via: create_document
id: materialization-guardas-lock
title: guardas lock
source_atoms:
- atom-apply-batch-prevalida-y-escribe-bajo-el-cerrojo-del-store-y-rechaza-con-conflicterror-un-guarda-obso
target_kind: code
target_identity: src/sldb/store/io/lock.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_apply_batch_lock.py
tags:
- system:sldb
- topic:store-lock
---

# guardas lock

## Intent

materializa en src/sldb/store/io/lock.py el atom atom-apply-batch-prevalida-y-escribe-bajo-el-cerrojo-del-store-y-rechaza-con-conflicterror-un-guarda-obso
