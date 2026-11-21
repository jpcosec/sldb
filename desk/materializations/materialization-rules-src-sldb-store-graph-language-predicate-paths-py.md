---
sldb:
  by: agent
  at: '2026-11-21T15:42:12Z'
  authority: generated
  via: create_document
id: materialization-rules-src-sldb-store-graph-language-predicate-paths-py
title: rules src-sldb-store-graph-language-predicate_paths-py
source_atoms:
- atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
target_kind: code
target_identity: src/sldb/store/graph/language/predicate_paths.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_rules.py tests/api/test_rules_evaluation.py
  tests/test_rules_language_spec.py
tags:
- system:sldb
- topic:rules
---

# rules src-sldb-store-graph-language-predicate_paths-py

## Intent

materializa en src/sldb/store/graph/language/predicate_paths.py el atom atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
