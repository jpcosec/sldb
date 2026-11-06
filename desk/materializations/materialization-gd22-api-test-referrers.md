---
id: materialization-gd22-api-test-referrers
title: gd22 api test_referrers
source_atoms:
- atom-las-referencias-entrantes-de-un-documento-se-consultan-y-se-reescriben-en-sldb-todo-o-nada
target_kind: test
target_identity: tests/api/test_referrers.py
validation:
- pytest -q tests/api/test_referrers.py
tags:
- system:sldb
- topic:references
---

# gd22 api test_referrers

## Intent

materializa atom-las-referencias-entrantes-de-un-documento-se-consultan-y-se-reescriben-en-sldb-todo-o-nada en tests/api/test_referrers.py
