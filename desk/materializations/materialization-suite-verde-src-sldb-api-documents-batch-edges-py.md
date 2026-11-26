---
sldb:
  by: agent
  at: '2026-11-26T13:26:54Z'
  authority: generated
  via: create_document
id: materialization-suite-verde-src-sldb-api-documents-batch-edges-py
title: suite-verde src-sldb-api-documents-batch_edges-py
source_atoms:
- atom-la-suite-de-sldb-vuelve-a-verde
target_kind: code
target_identity: src/sldb/api/documents/batch_edges.py
validation:
- pytest -q tests/test_clean_code_rules.py tests/api/test_api_creation.py tests/mcp/test_no_writes.py
tags:
- system:sldb
- topic:suite-verde
---

# suite-verde src-sldb-api-documents-batch_edges-py

## Intent

materializa en src/sldb/api/documents/batch_edges.py el atom atom-la-suite-de-sldb-vuelve-a-verde
