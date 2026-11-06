---
id: materialization-gd25-notation-view-doc-checks
title: gd25 notation view_doc_checks
source_atoms:
- atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta
target_kind: code
target_identity: src/sldb/models/notation/view_doc_checks.py
validation:
- pytest -q tests/api/test_views.py tests/api/test_view_doc.py
tags:
- system:sldb
- topic:views
---

# gd25 notation view_doc_checks

## Intent

materializa atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta en src/sldb/models/notation/view_doc_checks.py
