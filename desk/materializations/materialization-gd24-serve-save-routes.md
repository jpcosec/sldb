---
id: materialization-gd24-serve-save-routes
title: gd24 serve save_routes
source_atoms:
- atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
target_kind: code
target_identity: src/sldb/cli/serve/save_routes.py
validation:
- pytest -q tests/api/test_transaction.py tests/api/test_write_paths_validate.py
tags:
- system:sldb
- topic:transactions
---

# gd24 serve save_routes

## Intent

materializa la escritura todo o nada de GD24 en src/sldb/cli/serve/save_routes.py
