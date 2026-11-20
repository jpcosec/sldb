---
sldb:
  by: agent
  at: '2026-11-20T13:04:15Z'
  authority: generated
  via: create_document
id: materialization-rules-tests-api-test-rules-py
title: rules tests-api-test_rules-py
source_atoms:
- atom-save-document-payload-devuelve-las-alertas-on-write-de-la-escritura-y-la-regla-ve-las-aristas-del-pa
target_kind: test
target_identity: tests/api/test_rules.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_on_write_entering.py
  tests/api/test_rules.py
tags:
- system:sldb
- topic:rules
---

# rules tests-api-test_rules-py

## Intent

materializa en tests/api/test_rules.py el atom atom-save-document-payload-devuelve-las-alertas-on-write-de-la-escritura-y-la-regla-ve-las-aristas-del-pa
