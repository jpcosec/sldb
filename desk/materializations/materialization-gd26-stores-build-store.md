---
id: materialization-gd26-stores-build-store
title: gd26 stores build_store
source_atoms:
- atom-la-estructura-inicial-de-un-store-se-declara-como-carpetas-y-semillas
target_kind: code
target_identity: src/sldb/api/stores/build_store.py
validation:
- pytest -q tests/api/test_scaffold_store.py tests/store/test_stores_build.py
tags:
- system:sldb
- topic:scaffold
---

# gd26 stores build_store

## Intent

materializa el scaffold declarado de GD26 en src/sldb/api/stores/build_store.py
