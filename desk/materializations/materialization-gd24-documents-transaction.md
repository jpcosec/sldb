---
id: materialization-gd24-documents-transaction
title: gd24 documents transaction
source_atoms:
- atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
target_kind: code
target_identity: src/sldb/api/documents/transaction.py
validation:
- pytest -q tests/api/test_transaction.py tests/api/test_write_paths_validate.py
tags:
- system:sldb
- topic:transactions
---

# gd24 documents transaction

## Intent

materializa la escritura todo o nada de GD24 en src/sldb/api/documents/transaction.py
