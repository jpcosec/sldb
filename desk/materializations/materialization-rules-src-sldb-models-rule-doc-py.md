---
sldb:
  by: agent
  at: '2026-11-21T15:40:14Z'
  authority: generated
  via: create_document
id: materialization-rules-src-sldb-models-rule-doc-py
title: rules src-sldb-models-rule_doc-py
source_atoms:
- atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
target_kind: code
target_identity: src/sldb/models/rule_doc.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_rules.py tests/api/test_rules_evaluation.py
  tests/test_rules_language_spec.py
tags:
- system:sldb
- topic:rules
---

# rules src-sldb-models-rule_doc-py

## Intent

materializa en src/sldb/models/rule_doc.py el atom atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
