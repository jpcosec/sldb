---
sldb:
  by: agent
  at: '2026-11-20T15:29:56Z'
  authority: generated
  via: create_document
id: materialization-matching-src-sldb-api-matching-atoms-by-view-py
title: matching src-sldb-api-matching-atoms_by_view-py
source_atoms:
- atom-raw-atoms-by-view-si-se-pasa-atoms-dir-ese-directorio-manda-para-todas-las-vistas
target_kind: code
target_identity: src/sldb/api/matching/atoms_by_view.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/matching/test_matching_refs.py
tags:
- system:sldb
- topic:matching
---

# matching src-sldb-api-matching-atoms_by_view-py

## Intent

materializa en src/sldb/api/matching/atoms_by_view.py el atom atom-raw-atoms-by-view-si-se-pasa-atoms-dir-ese-directorio-manda-para-todas-las-vistas
