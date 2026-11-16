---
sldb:
  by: agent
  at: '2026-11-16T19:46:47Z'
  authority: generated
  via: create_document
id: materialization-guardas-test-apply-batch-lock
title: guardas test_apply_batch_lock
source_atoms:
- atom-apply-batch-prevalida-y-escribe-bajo-el-cerrojo-del-store-y-rechaza-con-conflicterror-un-guarda-obso
target_kind: test
target_identity: tests/api/test_apply_batch_lock.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_apply_batch_lock.py
tags:
- system:sldb
- topic:store-lock
---

# guardas test_apply_batch_lock

## Intent

materializa en tests/api/test_apply_batch_lock.py el atom atom-apply-batch-prevalida-y-escribe-bajo-el-cerrojo-del-store-y-rechaza-con-conflicterror-un-guarda-obso
