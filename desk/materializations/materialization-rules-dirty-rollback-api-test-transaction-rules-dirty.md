---
sldb:
  by: agent
  at: '2026-11-09T17:25:18Z'
  authority: generated
  via: create_document
id: materialization-rules-dirty-rollback-api-test-transaction-rules-dirty
title: rules-dirty-rollback api test_transaction_rules_dirty
source_atoms:
- atom-la-transacción-restaura-el-dirty-set-de-reglas-en-el-rollback
target_kind: test
target_identity: tests/api/test_transaction_rules_dirty.py
validation:
- pytest -q tests/api/test_transaction_rules_dirty.py
tags:
- system:sldb
- topic:transaction
---

# rules-dirty-rollback api test_transaction_rules_dirty

## Intent

materializa atom-la-transacción-restaura-el-dirty-set-de-reglas-en-el-rollback en tests/api/test_transaction_rules_dirty.py
