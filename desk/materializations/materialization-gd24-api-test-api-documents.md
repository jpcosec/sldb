---
id: materialization-gd24-api-test-api-documents
title: gd24 api test_api_documents
source_atoms:
- atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
target_kind: test
target_identity: tests/api/test_api_documents.py
validation:
- pytest -q tests/api/test_api_documents.py
tags:
- system:sldb
- topic:transactions
---

# gd24 api test_api_documents

## Intent

materializa la escritura todo o nada de GD24 en tests/api/test_api_documents.py
