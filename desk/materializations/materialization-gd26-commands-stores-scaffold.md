---
id: materialization-gd26-commands-stores-scaffold
title: gd26 commands stores_scaffold
source_atoms:
- atom-la-estructura-inicial-de-un-store-se-declara-como-carpetas-y-semillas
target_kind: code
target_identity: src/sldb/cli/commands/stores_scaffold.py
validation:
- pytest -q tests/api/test_scaffold_store.py tests/store/test_stores_build.py
tags:
- system:sldb
- topic:scaffold
---

# gd26 commands stores_scaffold

## Intent

materializa el scaffold declarado de GD26 en src/sldb/cli/commands/stores_scaffold.py
