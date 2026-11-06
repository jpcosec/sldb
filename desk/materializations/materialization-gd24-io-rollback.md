---
id: materialization-gd24-io-rollback
title: gd24 io rollback
source_atoms:
- atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
target_kind: code
target_identity: src/sldb/store/io/rollback.py
validation:
- pytest -q tests/api/test_transaction.py tests/api/test_write_paths_validate.py
tags:
- system:sldb
- topic:transactions
---

# gd24 io rollback

## Intent

materializa la escritura todo o nada de GD24 en src/sldb/store/io/rollback.py
