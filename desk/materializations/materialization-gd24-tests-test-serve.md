---
id: materialization-gd24-tests-test-serve
title: gd24 tests test_serve
source_atoms:
- atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
target_kind: test
target_identity: tests/test_serve.py
validation:
- pytest -q tests/test_serve.py
tags:
- system:sldb
- topic:transactions
---

# gd24 tests test_serve

## Intent

materializa la escritura todo o nada de GD24 en tests/test_serve.py
