---
id: materialization-gd22-api-test-rewrite-references
title: gd22 api test_rewrite_references
source_atoms:
- atom-las-referencias-entrantes-de-un-documento-se-consultan-y-se-reescriben-en-sldb-todo-o-nada
target_kind: test
target_identity: tests/api/test_rewrite_references.py
validation:
- pytest -q tests/api/test_rewrite_references.py
tags:
- system:sldb
- topic:references
---

# gd22 api test_rewrite_references

## Intent

materializa atom-las-referencias-entrantes-de-un-documento-se-consultan-y-se-reescriben-en-sldb-todo-o-nada en tests/api/test_rewrite_references.py
