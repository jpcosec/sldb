---
sldb:
  by: agent
  at: '2026-11-20T15:30:24Z'
  authority: generated
  via: create_document
id: materialization-matching-tests-matching-test-matching-refs-py
title: matching tests-matching-test_matching_refs-py
source_atoms:
- atom-raw-atoms-by-view-si-se-pasa-atoms-dir-ese-directorio-manda-para-todas-las-vistas
target_kind: test
target_identity: tests/matching/test_matching_refs.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/matching/test_matching_refs.py
tags:
- system:sldb
- topic:matching
---

# matching tests-matching-test_matching_refs-py

## Intent

materializa en tests/matching/test_matching_refs.py el atom atom-raw-atoms-by-view-si-se-pasa-atoms-dir-ese-directorio-manda-para-todas-las-vistas
