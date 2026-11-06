---
id: materialization-gd24-api-test-transaction
title: gd24 api test_transaction
source_atoms:
- atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
target_kind: test
target_identity: tests/api/test_transaction.py
validation:
- pytest -q tests/api/test_transaction.py
tags:
- system:sldb
- topic:transactions
---

# gd24 api test_transaction

## Intent

materializa la escritura todo o nada de GD24 en tests/api/test_transaction.py
