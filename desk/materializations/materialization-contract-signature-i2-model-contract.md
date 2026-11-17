---
sldb:
  by: agent
  at: '2026-11-17T01:04:32Z'
  authority: generated
  via: create_document
id: materialization-contract-signature-i2-model-contract
title: contract-signature-i2 model_contract
source_atoms:
- atom-lo-que-la-clase-declara-se-relee-cada-vez-que-el-store-firma-el-modelo
target_kind: code
target_identity: src/sldb/store/model_contract.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_payload_projection.py
  tests/api/test_doc_anchors.py
tags:
- system:sldb
- topic:store
---

# contract-signature-i2 model_contract

## Intent

materializa en src/sldb/store/model_contract.py el atom atom-lo-que-la-clase-declara-se-relee-cada-vez-que-el-store-firma-el-modelo
