---
id: materialization-gd24-documents-transaction-paths
title: gd24 documents transaction_paths
source_atoms:
- atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
target_kind: code
target_identity: src/sldb/api/documents/transaction_paths.py
validation:
- pytest -q tests/api/test_transaction.py tests/api/test_write_paths_validate.py
tags:
- system:sldb
- topic:transactions
---

# gd24 documents transaction_paths

## Intent

materializa la escritura todo o nada de GD24 en src/sldb/api/documents/transaction_paths.py
