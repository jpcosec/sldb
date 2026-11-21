---
sldb:
  by: agent
  at: '2026-11-21T15:44:12Z'
  authority: generated
  via: create_document
id: materialization-rules-tests-test-rules-language-spec-py
title: rules tests-test_rules_language_spec-py
source_atoms:
- atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
target_kind: test
target_identity: tests/test_rules_language_spec.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_rules.py tests/api/test_rules_evaluation.py
  tests/test_rules_language_spec.py
tags:
- system:sldb
- topic:rules
---

# rules tests-test_rules_language_spec-py

## Intent

materializa en tests/test_rules_language_spec.py el atom atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
