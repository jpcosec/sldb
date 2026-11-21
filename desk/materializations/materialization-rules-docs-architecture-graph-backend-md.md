---
sldb:
  by: agent
  at: '2026-11-21T15:35:19Z'
  authority: generated
  via: create_document
id: materialization-rules-docs-architecture-graph-backend-md
title: rules docs-architecture-graph-backend-md
source_atoms:
- atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
target_kind: docs
target_identity: docs/architecture/graph-backend.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_rules.py tests/api/test_rules_evaluation.py
  tests/test_rules_language_spec.py
tags:
- system:sldb
- topic:rules
---

# rules docs-architecture-graph-backend-md

## Intent

materializa en docs/architecture/graph-backend.md el atom atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
