---
id: materialization-gd23-query-engine-structural-queries
title: gd23 query_engine structural_queries
source_atoms:
- atom-un-documento-se-elige-con-un-selector-declarado-y-la-ambigüedad-es-un-error
target_kind: code
target_identity: src/sldb/store/query_engine/structural_queries.py
validation:
- pytest -q tests/api/test_select_documents.py
tags:
- system:sldb
- topic:selectors
---

# gd23 query_engine structural_queries

## Intent

materializa la selección declarada de documentos de GD23 en src/sldb/store/query_engine/structural_queries.py
