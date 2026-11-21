---
sldb:
  by: agent
  at: '2026-11-21T12:16:33Z'
  authority: generated
  via: create_document
id: materialization-store-tests-store-test-merkle-operation-cache-py
title: store tests-store-test_merkle_operation_cache-py
source_atoms:
- atom-el-conjunto-de-documentos-sucios-se-persiste-en-sldb
target_kind: test
target_identity: tests/store/test_merkle_operation_cache.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests
tags:
- system:sldb
- topic:store
---

# store tests-store-test_merkle_operation_cache-py

## Intent

materializa en tests/store/test_merkle_operation_cache.py el atom atom-el-conjunto-de-documentos-sucios-se-persiste-en-sldb
