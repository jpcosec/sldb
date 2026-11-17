---
sldb:
  by: agent
  at: '2026-11-17T13:59:16Z'
  authority: generated
  via: create_document
id: materialization-orph-test-apply-batch-lock
title: orph test_apply_batch_lock
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

# orph test_apply_batch_lock

## Intent

materializa en tests/api/test_apply_batch_lock.py el atom atom-apply-batch-prevalida-y-escribe-bajo-el-cerrojo-del-store-y-rechaza-con-conflicterror-un-guarda-obso
