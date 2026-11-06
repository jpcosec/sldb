---
id: materialization-gd24-tests-test-serve-auth
title: gd24 tests test_serve_auth
source_atoms:
- atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
target_kind: test
target_identity: tests/test_serve_auth.py
validation:
- pytest -q tests/test_serve_auth.py
tags:
- system:sldb
- topic:transactions
---

# gd24 tests test_serve_auth

## Intent

materializa la escritura todo o nada de GD24 en tests/test_serve_auth.py
