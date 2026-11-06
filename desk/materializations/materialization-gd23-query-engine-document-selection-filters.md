---
id: materialization-gd23-query-engine-document-selection-filters
title: gd23 query_engine document_selection_filters
source_atoms:
- atom-un-documento-se-elige-con-un-selector-declarado-y-la-ambigüedad-es-un-error
target_kind: code
target_identity: src/sldb/store/query_engine/document_selection_filters.py
validation:
- pytest -q tests/api/test_select_documents.py
tags:
- system:sldb
- topic:selectors
---

# gd23 query_engine document_selection_filters

## Intent

materializa la selección declarada de documentos de GD23 en src/sldb/store/query_engine/document_selection_filters.py
