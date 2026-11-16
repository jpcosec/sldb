---
sldb:
  by: agent
  at: '2026-11-16T20:32:59Z'
  authority: generated
  via: create_document
id: materialization-inverso-test-transaction
title: inverso test_transaction
source_atoms:
- atom-apply-batch-devuelve-en-batchreport-inverse-el-lote-que-lo-deshace-con-guardas
target_kind: test
target_identity: tests/api/test_transaction.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_transaction.py
tags:
- system:sldb
- topic:batch
---

# inverso test_transaction

## Intent

materializa en tests/api/test_transaction.py el atom atom-apply-batch-devuelve-en-batchreport-inverse-el-lote-que-lo-deshace-con-guardas
