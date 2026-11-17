---
sldb:
  by: agent
  at: '2026-11-17T01:05:18Z'
  authority: generated
  via: create_document
id: materialization-contract-signature-i2-doc-anchor-value
title: contract-signature-i2 doc_anchor_value
source_atoms:
- atom-lo-que-la-clase-declara-se-relee-cada-vez-que-el-store-firma-el-modelo
target_kind: code
target_identity: src/sldb/models/doc_anchor_value.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_payload_projection.py
  tests/api/test_doc_anchors.py
tags:
- system:sldb
- topic:store
---

# contract-signature-i2 doc_anchor_value

## Intent

materializa en src/sldb/models/doc_anchor_value.py el atom atom-lo-que-la-clase-declara-se-relee-cada-vez-que-el-store-firma-el-modelo
