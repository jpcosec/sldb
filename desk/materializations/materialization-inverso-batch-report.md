---
sldb:
  by: agent
  at: '2026-11-16T20:32:34Z'
  authority: generated
  via: create_document
id: materialization-inverso-batch-report
title: inverso batch_report
source_atoms:
- atom-apply-batch-devuelve-en-batchreport-inverse-el-lote-que-lo-deshace-con-guardas
target_kind: code
target_identity: src/sldb/api/documents/batch_report.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_transaction.py
tags:
- system:sldb
- topic:batch
---

# inverso batch_report

## Intent

materializa en src/sldb/api/documents/batch_report.py el atom atom-apply-batch-devuelve-en-batchreport-inverse-el-lote-que-lo-deshace-con-guardas
