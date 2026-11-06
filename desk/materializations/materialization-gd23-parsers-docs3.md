---
id: materialization-gd23-parsers-docs3
title: gd23 parsers docs3
source_atoms:
- atom-un-documento-se-elige-con-un-selector-declarado-y-la-ambigüedad-es-un-error
target_kind: code
target_identity: src/sldb/cli/parsers/docs3.py
validation:
- pytest -q tests/api/test_select_documents.py
tags:
- system:sldb
- topic:selectors
---

# gd23 parsers docs3

## Intent

materializa la selección declarada de documentos de GD23 en src/sldb/cli/parsers/docs3.py
