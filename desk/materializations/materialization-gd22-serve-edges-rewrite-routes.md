---
id: materialization-gd22-serve-edges-rewrite-routes
title: gd22 serve edges_rewrite_routes
source_atoms:
- atom-las-referencias-entrantes-de-un-documento-se-consultan-y-se-reescriben-en-sldb-todo-o-nada
target_kind: code
target_identity: src/sldb/cli/serve/edges_rewrite_routes.py
validation:
- pytest -q tests/api/test_referrers.py tests/api/test_rewrite_references.py
tags:
- system:sldb
- topic:references
---

# gd22 serve edges_rewrite_routes

## Intent

materializa atom-las-referencias-entrantes-de-un-documento-se-consultan-y-se-reescriben-en-sldb-todo-o-nada en src/sldb/cli/serve/edges_rewrite_routes.py
