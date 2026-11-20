---
sldb:
  by: agent
  at: '2026-11-20T13:03:07Z'
  authority: generated
  via: create_document
id: materialization-rules-src-sldb-api-rules-rules-on-write-py
title: rules src-sldb-api-rules-rules_on_write-py
source_atoms:
- atom-save-document-payload-devuelve-las-alertas-on-write-de-la-escritura-y-la-regla-ve-las-aristas-del-pa
target_kind: code
target_identity: src/sldb/api/rules/rules_on_write.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_on_write_entering.py
  tests/api/test_rules.py
tags:
- system:sldb
- topic:rules
---

# rules src-sldb-api-rules-rules_on_write-py

## Intent

materializa en src/sldb/api/rules/rules_on_write.py el atom atom-save-document-payload-devuelve-las-alertas-on-write-de-la-escritura-y-la-regla-ve-las-aristas-del-pa
