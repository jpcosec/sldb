---
sldb:
  by: agent
  at: '2026-11-21T14:27:31Z'
  authority: generated
  via: create_document
id: materialization-store-src-sldb-api-documents-transaction-state-py
title: store src-sldb-api-documents-transaction_state-py
source_atoms:
- atom-el-rollback-de-una-transaccion-restaura-el-conjunto-sucio-persistido
target_kind: code
target_identity: src/sldb/api/documents/transaction_state.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider -n 4 tests/api tests/store/test_merkle_operation_cache.py
tags:
- system:sldb
- topic:store
---

# store src-sldb-api-documents-transaction_state-py

## Intent

materializa en src/sldb/api/documents/transaction_state.py el atom atom-el-rollback-de-una-transaccion-restaura-el-conjunto-sucio-persistido
