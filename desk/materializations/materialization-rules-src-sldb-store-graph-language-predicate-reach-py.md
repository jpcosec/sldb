---
sldb:
  by: agent
  at: '2026-11-21T15:42:42Z'
  authority: generated
  via: create_document
id: materialization-rules-src-sldb-store-graph-language-predicate-reach-py
title: rules src-sldb-store-graph-language-predicate_reach-py
source_atoms:
- atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
target_kind: code
target_identity: src/sldb/store/graph/language/predicate_reach.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_rules.py tests/api/test_rules_evaluation.py
  tests/test_rules_language_spec.py
tags:
- system:sldb
- topic:rules
---

# rules src-sldb-store-graph-language-predicate_reach-py

## Intent

materializa en src/sldb/store/graph/language/predicate_reach.py el atom atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
