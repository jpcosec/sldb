---
sldb:
  by: agent
  at: '2026-11-17T01:06:05Z'
  authority: generated
  via: create_document
id: materialization-contract-signature-i2-test-doc-anchors
title: contract-signature-i2 test_doc_anchors
source_atoms:
- atom-lo-que-la-clase-declara-se-relee-cada-vez-que-el-store-firma-el-modelo
target_kind: test
target_identity: tests/api/test_doc_anchors.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_payload_projection.py
  tests/api/test_doc_anchors.py
tags:
- system:sldb
- topic:store
---

# contract-signature-i2 test_doc_anchors

## Intent

materializa en tests/api/test_doc_anchors.py el atom atom-lo-que-la-clase-declara-se-relee-cada-vez-que-el-store-firma-el-modelo
