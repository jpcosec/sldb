---
id: materialization-gd26-parsers-stores
title: gd26 parsers stores
source_atoms:
- atom-la-estructura-inicial-de-un-store-se-declara-como-carpetas-y-semillas
target_kind: code
target_identity: src/sldb/cli/parsers/stores.py
validation:
- pytest -q tests/api/test_scaffold_store.py tests/store/test_stores_build.py
tags:
- system:sldb
- topic:scaffold
---

# gd26 parsers stores

## Intent

materializa el scaffold declarado de GD26 en src/sldb/cli/parsers/stores.py
