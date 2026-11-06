---
id: materialization-gd25-api-test-views
title: gd25 api test_views
source_atoms:
- atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta
target_kind: test
target_identity: tests/api/test_views.py
validation:
- pytest -q tests/api/test_views.py
tags:
- system:sldb
- topic:views
---

# gd25 api test_views

## Intent

materializa atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta en tests/api/test_views.py
