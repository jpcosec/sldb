---
id: materialization-gd24-commands-fields-save
title: gd24 commands fields_save
source_atoms:
- atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
target_kind: code
target_identity: src/sldb/cli/commands/fields_save.py
validation:
- pytest -q tests/api/test_transaction.py tests/api/test_write_paths_validate.py
tags:
- system:sldb
- topic:transactions
---

# gd24 commands fields_save

## Intent

materializa la escritura todo o nada de GD24 en src/sldb/cli/commands/fields_save.py
