---
sldb:
  by: agent
  at: '2026-11-16T15:56:12Z'
  authority: generated
  via: create_document
id: materialization-c3-createpin-create-document
title: c3-createpin create_document
source_atoms:
- atom-crear-un-documento-ya-fija-sus-anclas-a-documentos-create-document-pinnea-igual-que-save-document-pa
target_kind: code
target_identity: src/sldb/api/documents/create_document.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
tags:
- system:sldb
- topic:clean-code
---

# c3-createpin create_document

## Intent

materializa en src/sldb/api/documents/create_document.py el atom atom-crear-un-documento-ya-fija-sus-anclas-a-documentos-create-document-pinnea-igual-que-save-document-pa
