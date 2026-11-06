---
id: materialization-gd24-documents-move-document
title: gd24 documents move_document
source_atoms:
- atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
target_kind: code
target_identity: src/sldb/api/documents/move_document.py
validation:
- pytest -q tests/api/test_transaction.py tests/api/test_write_paths_validate.py
tags:
- system:sldb
- topic:transactions
---

# gd24 documents move_document

## Intent

materializa la escritura todo o nada de GD24 en src/sldb/api/documents/move_document.py
