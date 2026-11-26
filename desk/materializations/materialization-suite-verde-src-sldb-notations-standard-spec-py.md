---
sldb:
  by: agent
  at: '2026-11-26T13:31:08Z'
  authority: generated
  via: create_document
id: materialization-suite-verde-src-sldb-notations-standard-spec-py
title: suite-verde src-sldb-notations-standard_spec-py
source_atoms:
- atom-la-suite-de-sldb-vuelve-a-verde
target_kind: code
target_identity: src/sldb/notations/standard_spec.py
validation:
- pytest -q tests/test_clean_code_rules.py tests/api/test_api_creation.py tests/mcp/test_no_writes.py
tags:
- system:sldb
- topic:suite-verde
---

# suite-verde src-sldb-notations-standard_spec-py

## Intent

materializa en src/sldb/notations/standard_spec.py el atom atom-la-suite-de-sldb-vuelve-a-verde
