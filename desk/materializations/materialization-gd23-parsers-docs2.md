---
id: materialization-gd23-parsers-docs2
title: gd23 parsers docs2
source_atoms:
- atom-un-documento-se-elige-con-un-selector-declarado-y-la-ambigüedad-es-un-error
target_kind: code
target_identity: src/sldb/cli/parsers/docs2.py
validation:
- pytest -q tests/api/test_select_documents.py
tags:
- system:sldb
- topic:selectors
---

# gd23 parsers docs2

## Intent

materializa la selección declarada de documentos de GD23 en src/sldb/cli/parsers/docs2.py
