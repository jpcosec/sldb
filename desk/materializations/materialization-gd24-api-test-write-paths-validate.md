---
id: materialization-gd24-api-test-write-paths-validate
title: gd24 api test_write_paths_validate
source_atoms:
- atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
target_kind: test
target_identity: tests/api/test_write_paths_validate.py
validation:
- pytest -q tests/api/test_write_paths_validate.py
tags:
- system:sldb
- topic:transactions
---

# gd24 api test_write_paths_validate

## Intent

materializa la escritura todo o nada de GD24 en tests/api/test_write_paths_validate.py
