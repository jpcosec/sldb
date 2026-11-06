---
id: materialization-gd23-api-test-select-documents
title: gd23 api test_select_documents
source_atoms:
- atom-un-documento-se-elige-con-un-selector-declarado-y-la-ambigüedad-es-un-error
target_kind: test
target_identity: tests/api/test_select_documents.py
validation:
- pytest -q tests/api/test_select_documents.py
tags:
- system:sldb
- topic:selectors
---

# gd23 api test_select_documents

## Intent

materializa la selección declarada de documentos de GD23 en tests/api/test_select_documents.py
