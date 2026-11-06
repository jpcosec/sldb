---
id: materialization-gd26-stores-scaffold-report
title: gd26 stores scaffold_report
source_atoms:
- atom-la-estructura-inicial-de-un-store-se-declara-como-carpetas-y-semillas
target_kind: code
target_identity: src/sldb/api/stores/scaffold_report.py
validation:
- pytest -q tests/api/test_scaffold_store.py tests/store/test_stores_build.py
tags:
- system:sldb
- topic:scaffold
---

# gd26 stores scaffold_report

## Intent

materializa el scaffold declarado de GD26 en src/sldb/api/stores/scaffold_report.py
