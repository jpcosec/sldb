---
sldb:
  by: agent
  at: '2026-11-16T19:45:35Z'
  authority: generated
  via: create_document
id: materialization-guardas-apply-batch
title: guardas apply_batch
source_atoms:
- atom-apply-batch-prevalida-y-escribe-bajo-el-cerrojo-del-store-y-rechaza-con-conflicterror-un-guarda-obso
target_kind: code
target_identity: src/sldb/api/documents/apply_batch.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_apply_batch_lock.py
tags:
- system:sldb
- topic:store-lock
---

# guardas apply_batch

## Intent

materializa en src/sldb/api/documents/apply_batch.py el atom atom-apply-batch-prevalida-y-escribe-bajo-el-cerrojo-del-store-y-rechaza-con-conflicterror-un-guarda-obso
