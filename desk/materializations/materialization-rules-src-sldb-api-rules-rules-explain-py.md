---
sldb:
  by: agent
  at: '2026-11-21T15:38:17Z'
  authority: generated
  via: create_document
id: materialization-rules-src-sldb-api-rules-rules-explain-py
title: rules src-sldb-api-rules-rules_explain-py
source_atoms:
- atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
target_kind: code
target_identity: src/sldb/api/rules/rules_explain.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_rules.py tests/api/test_rules_evaluation.py
  tests/test_rules_language_spec.py
tags:
- system:sldb
- topic:rules
---

# rules src-sldb-api-rules-rules_explain-py

## Intent

materializa en src/sldb/api/rules/rules_explain.py el atom atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
