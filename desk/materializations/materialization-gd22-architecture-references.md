---
id: materialization-gd22-architecture-references
title: gd22 architecture references
source_atoms:
- atom-las-referencias-entrantes-de-un-documento-se-consultan-y-se-reescriben-en-sldb-todo-o-nada
target_kind: doc
target_identity: docs/architecture/references.md
validation:
- pytest -q tests/api/test_referrers.py tests/api/test_rewrite_references.py
tags:
- system:sldb
- topic:references
---

# gd22 architecture references

## Intent

materializa atom-las-referencias-entrantes-de-un-documento-se-consultan-y-se-reescriben-en-sldb-todo-o-nada en docs/architecture/references.md
