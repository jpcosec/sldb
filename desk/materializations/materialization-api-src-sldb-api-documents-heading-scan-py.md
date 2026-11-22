---
sldb:
  by: agent
  at: '2026-11-22T13:17:57Z'
  authority: generated
  via: create_document
id: materialization-api-src-sldb-api-documents-heading-scan-py
title: api src-sldb-api-documents-heading_scan-py
source_atoms:
- atom-scan-heading-bodies-cumple-la-regla-de-codigo-limpio
target_kind: code
target_identity: src/sldb/api/documents/heading_scan.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_clean_code_rules.py
  tests/api/test_lossy_overwrite_content.py
tags:
- system:sldb
- topic:api
---

# api src-sldb-api-documents-heading_scan-py

## Intent

materializa en src/sldb/api/documents/heading_scan.py el atom atom-scan-heading-bodies-cumple-la-regla-de-codigo-limpio
