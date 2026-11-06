---
id: materialization-gd24-exceptions-init
title: gd24 exceptions __init__
source_atoms:
- atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
target_kind: code
target_identity: src/sldb/core/exceptions/__init__.py
validation:
- pytest -q tests/api/test_transaction.py tests/api/test_write_paths_validate.py
tags:
- system:sldb
- topic:transactions
---

# gd24 exceptions __init__

## Intent

materializa la escritura todo o nada de GD24 en src/sldb/core/exceptions/__init__.py
