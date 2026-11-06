---
id: materialization-gd23-serve-docs-select-routes
title: gd23 serve docs_select_routes
source_atoms:
- atom-un-documento-se-elige-con-un-selector-declarado-y-la-ambigüedad-es-un-error
target_kind: code
target_identity: src/sldb/cli/serve/docs_select_routes.py
validation:
- pytest -q tests/api/test_select_documents.py
tags:
- system:sldb
- topic:selectors
---

# gd23 serve docs_select_routes

## Intent

materializa la selección declarada de documentos de GD23 en src/sldb/cli/serve/docs_select_routes.py
