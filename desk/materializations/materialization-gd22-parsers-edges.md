---
id: materialization-gd22-parsers-edges
title: gd22 parsers edges
source_atoms:
- atom-las-referencias-entrantes-de-un-documento-se-consultan-y-se-reescriben-en-sldb-todo-o-nada
target_kind: code
target_identity: src/sldb/cli/parsers/edges.py
validation:
- pytest -q tests/api/test_referrers.py tests/api/test_rewrite_references.py
tags:
- system:sldb
- topic:references
---

# gd22 parsers edges

## Intent

materializa atom-las-referencias-entrantes-de-un-documento-se-consultan-y-se-reescriben-en-sldb-todo-o-nada en src/sldb/cli/parsers/edges.py
