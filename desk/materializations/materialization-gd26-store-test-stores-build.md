---
id: materialization-gd26-store-test-stores-build
title: gd26 store test_stores_build
source_atoms:
- atom-la-estructura-inicial-de-un-store-se-declara-como-carpetas-y-semillas
target_kind: test
target_identity: tests/store/test_stores_build.py
validation:
- pytest -q tests/store/test_stores_build.py
tags:
- system:sldb
- topic:scaffold
---

# gd26 store test_stores_build

## Intent

materializa el scaffold declarado de GD26 en tests/store/test_stores_build.py
