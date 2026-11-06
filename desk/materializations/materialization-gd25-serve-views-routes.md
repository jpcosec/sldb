---
id: materialization-gd25-serve-views-routes
title: gd25 serve views_routes
source_atoms:
- atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta
target_kind: code
target_identity: src/sldb/cli/serve/views_routes.py
validation:
- pytest -q tests/api/test_views.py tests/api/test_view_doc.py
tags:
- system:sldb
- topic:views
---

# gd25 serve views_routes

## Intent

materializa atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta en src/sldb/cli/serve/views_routes.py
