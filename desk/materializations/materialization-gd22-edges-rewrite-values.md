---
id: materialization-gd22-edges-rewrite-values
title: gd22 edges rewrite_values
source_atoms:
- atom-las-referencias-entrantes-de-un-documento-se-consultan-y-se-reescriben-en-sldb-todo-o-nada
target_kind: code
target_identity: src/sldb/api/edges/rewrite_values.py
validation:
- pytest -q tests/api/test_referrers.py tests/api/test_rewrite_references.py
tags:
- system:sldb
- topic:references
---

# gd22 edges rewrite_values

## Intent

materializa atom-las-referencias-entrantes-de-un-documento-se-consultan-y-se-reescriben-en-sldb-todo-o-nada en src/sldb/api/edges/rewrite_values.py
