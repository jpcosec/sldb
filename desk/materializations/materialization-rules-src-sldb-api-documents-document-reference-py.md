---
sldb:
  by: agent
  at: '2026-11-20T13:00:50Z'
  authority: generated
  via: create_document
id: materialization-rules-src-sldb-api-documents-document-reference-py
title: rules src-sldb-api-documents-document_reference-py
source_atoms:
- atom-save-document-payload-devuelve-las-alertas-on-write-de-la-escritura-y-la-regla-ve-las-aristas-del-pa
target_kind: code
target_identity: src/sldb/api/documents/document_reference.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_on_write_entering.py
  tests/api/test_rules.py
tags:
- system:sldb
- topic:rules
---

# rules src-sldb-api-documents-document_reference-py

## Intent

materializa en src/sldb/api/documents/document_reference.py el atom atom-save-document-payload-devuelve-las-alertas-on-write-de-la-escritura-y-la-regla-ve-las-aristas-del-pa
