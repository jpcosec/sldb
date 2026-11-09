---
sldb:
  by: agent
  at: '2026-11-09T17:25:14Z'
  authority: generated
  via: create_document
id: materialization-rules-dirty-rollback-documents-transaction-state
title: rules-dirty-rollback documents transaction_state
source_atoms:
- atom-la-transacción-restaura-el-dirty-set-de-reglas-en-el-rollback
target_kind: code
target_identity: src/sldb/api/documents/transaction_state.py
validation:
- pytest -q tests/api/test_transaction_rules_dirty.py
tags:
- system:sldb
- topic:transaction
---

# rules-dirty-rollback documents transaction_state

## Intent

materializa atom-la-transacción-restaura-el-dirty-set-de-reglas-en-el-rollback en src/sldb/api/documents/transaction_state.py
