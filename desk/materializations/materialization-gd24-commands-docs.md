---
id: materialization-gd24-commands-docs
title: gd24 commands docs
source_atoms:
- atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
target_kind: code
target_identity: src/sldb/cli/commands/docs.py
validation:
- pytest -q tests/api/test_transaction.py tests/api/test_write_paths_validate.py
tags:
- system:sldb
- topic:transactions
---

# gd24 commands docs

## Intent

materializa la escritura todo o nada de GD24 en src/sldb/cli/commands/docs.py
