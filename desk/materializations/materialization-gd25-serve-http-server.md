---
id: materialization-gd25-serve-http-server
title: gd25 serve http_server
source_atoms:
- atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta
target_kind: code
target_identity: src/sldb/cli/serve/http_server.py
validation:
- pytest -q tests/api/test_views.py tests/api/test_view_doc.py
tags:
- system:sldb
- topic:views
---

# gd25 serve http_server

## Intent

materializa atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta en src/sldb/cli/serve/http_server.py
