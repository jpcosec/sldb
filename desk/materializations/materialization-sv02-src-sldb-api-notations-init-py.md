---
id: materialization-sv02-src-sldb-api-notations-init-py
title: 'SV02: src/sldb/api/notations/__init__.py'
source_atoms:
- atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve
target_kind: code
target_identity: src/sldb/api/notations/__init__.py
validation:
- pytest -q tests/notations/test_notation_view_and_routes.py
tags:
- system:sldb
- task:sv02
---

# SV02: src/sldb/api/notations/__init__.py

## Intent

src/sldb/api/notations/__init__.py materializa la decision de SV02 (atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve).
