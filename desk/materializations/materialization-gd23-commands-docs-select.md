---
id: materialization-gd23-commands-docs-select
title: gd23 commands docs_select
source_atoms:
- atom-un-documento-se-elige-con-un-selector-declarado-y-la-ambigüedad-es-un-error
target_kind: code
target_identity: src/sldb/cli/commands/docs_select.py
validation:
- pytest -q tests/api/test_select_documents.py
tags:
- system:sldb
- topic:selectors
---

# gd23 commands docs_select

## Intent

materializa la selección declarada de documentos de GD23 en src/sldb/cli/commands/docs_select.py
