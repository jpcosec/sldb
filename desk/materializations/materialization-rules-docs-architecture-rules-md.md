---
sldb:
  by: agent
  at: '2026-11-21T15:35:51Z'
  authority: generated
  via: create_document
id: materialization-rules-docs-architecture-rules-md
title: rules docs-architecture-rules-md
source_atoms:
- atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
target_kind: docs
target_identity: docs/architecture/rules.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_rules.py tests/api/test_rules_evaluation.py
  tests/test_rules_language_spec.py
tags:
- system:sldb
- topic:rules
---

# rules docs-architecture-rules-md

## Intent

materializa en docs/architecture/rules.md el atom atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
