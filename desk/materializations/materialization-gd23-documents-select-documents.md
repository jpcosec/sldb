---
id: materialization-gd23-documents-select-documents
title: gd23 documents select_documents
source_atoms:
- atom-un-documento-se-elige-con-un-selector-declarado-y-la-ambigüedad-es-un-error
target_kind: code
target_identity: src/sldb/api/documents/select_documents.py
validation:
- pytest -q tests/api/test_select_documents.py
tags:
- system:sldb
- topic:selectors
---

# gd23 documents select_documents

## Intent

materializa la selección declarada de documentos de GD23 en src/sldb/api/documents/select_documents.py
