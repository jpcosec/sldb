---
id: materialization-gd24-documents-apply-batch
title: gd24 documents apply_batch
source_atoms:
- atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
target_kind: code
target_identity: src/sldb/api/documents/apply_batch.py
validation:
- pytest -q tests/api/test_transaction.py tests/api/test_write_paths_validate.py
tags:
- system:sldb
- topic:transactions
---

# gd24 documents apply_batch

## Intent

materializa la escritura todo o nada de GD24 en src/sldb/api/documents/apply_batch.py
