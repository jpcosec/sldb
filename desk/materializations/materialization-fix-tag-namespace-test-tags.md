---
sldb:
  by: agent
  at: '2026-11-19T12:43:58Z'
  authority: generated
  via: create_document
id: materialization-fix-tag-namespace-test-tags
title: fix tag_namespace test_tags
source_atoms:
- atom-los-hallazgos-builtin-tag-namespace-traen-un-fix-accionable
target_kind: test
target_identity: tests/api/test_tags.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_tags.py
tags:
- system:sldb
- topic:tags
---

# fix tag_namespace test_tags

## Intent

materializa en tests/api/test_tags.py el atom atom-los-hallazgos-builtin-tag-namespace-traen-un-fix-accionable
