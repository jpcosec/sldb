---
sldb:
  by: agent
  at: '2026-11-16T20:31:46Z'
  authority: generated
  via: create_document
id: materialization-inverso-apply-batch
title: inverso apply_batch
source_atoms:
- atom-apply-batch-devuelve-en-batchreport-inverse-el-lote-que-lo-deshace-con-guardas
target_kind: code
target_identity: src/sldb/api/documents/apply_batch.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_transaction.py
tags:
- system:sldb
- topic:batch
---

# inverso apply_batch

## Intent

materializa en src/sldb/api/documents/apply_batch.py el atom atom-apply-batch-devuelve-en-batchreport-inverse-el-lote-que-lo-deshace-con-guardas
