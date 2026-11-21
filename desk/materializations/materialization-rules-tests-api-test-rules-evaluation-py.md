---
sldb:
  by: agent
  at: '2026-11-21T15:43:43Z'
  authority: generated
  via: create_document
id: materialization-rules-tests-api-test-rules-evaluation-py
title: rules tests-api-test_rules_evaluation-py
source_atoms:
- atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
target_kind: test
target_identity: tests/api/test_rules_evaluation.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_rules.py tests/api/test_rules_evaluation.py
  tests/test_rules_language_spec.py
tags:
- system:sldb
- topic:rules
---

# rules tests-api-test_rules_evaluation-py

## Intent

materializa en tests/api/test_rules_evaluation.py el atom atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
