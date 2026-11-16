---
sldb:
  by: agent
  at: '2026-11-16T11:10:19Z'
  authority: generated
  via: create_document
id: materialization-create-pin-create-document
title: create-pin create_document
source_atoms:
- atom-crear-un-documento-ya-fija-sus-anclas-a-documentos-create-document-pinnea-igual-que-save-document-pa
target_kind: code
target_identity: src/sldb/api/documents/create_document.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_doc_anchors.py
  tests/api/test_on_write_entering.py
tags:
- system:sldb
- topic:anchors
---

# create-pin create_document

## Intent

materializa en src/sldb/api/documents/create_document.py el atom atom-crear-un-documento-ya-fija-sus-anclas-a-documentos-create-document-pinnea-igual-que-save-document-pa
