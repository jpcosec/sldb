---
id: materialization-gd24-commands-fields-mutate
title: gd24 commands fields_mutate
source_atoms:
- atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
target_kind: code
target_identity: src/sldb/cli/commands/fields_mutate.py
validation:
- pytest -q tests/api/test_transaction.py tests/api/test_write_paths_validate.py
tags:
- system:sldb
- topic:transactions
---

# gd24 commands fields_mutate

## Intent

materializa la escritura todo o nada de GD24 en src/sldb/cli/commands/fields_mutate.py
