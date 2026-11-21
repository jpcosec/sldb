---
sldb:
  by: agent
  at: '2026-11-21T15:41:14Z'
  authority: generated
  via: create_document
id: materialization-rules-src-sldb-store-graph-language-predicate-eval-py
title: rules src-sldb-store-graph-language-predicate_eval-py
source_atoms:
- atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
target_kind: code
target_identity: src/sldb/store/graph/language/predicate_eval.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_rules.py tests/api/test_rules_evaluation.py
  tests/test_rules_language_spec.py
tags:
- system:sldb
- topic:rules
---

# rules src-sldb-store-graph-language-predicate_eval-py

## Intent

materializa en src/sldb/store/graph/language/predicate_eval.py el atom atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
