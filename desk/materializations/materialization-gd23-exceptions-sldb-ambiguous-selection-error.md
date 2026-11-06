---
id: materialization-gd23-exceptions-sldb-ambiguous-selection-error
title: gd23 exceptions sldb_ambiguous_selection_error
source_atoms:
- atom-un-documento-se-elige-con-un-selector-declarado-y-la-ambigüedad-es-un-error
target_kind: code
target_identity: src/sldb/core/exceptions/sldb_ambiguous_selection_error.py
validation:
- pytest -q tests/api/test_select_documents.py
tags:
- system:sldb
- topic:selectors
---

# gd23 exceptions sldb_ambiguous_selection_error

## Intent

materializa la selección declarada de documentos de GD23 en src/sldb/core/exceptions/sldb_ambiguous_selection_error.py
