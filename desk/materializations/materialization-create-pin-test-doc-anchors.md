---
sldb:
  by: agent
  at: '2026-11-16T11:10:40Z'
  authority: generated
  via: create_document
id: materialization-create-pin-test-doc-anchors
title: create-pin test_doc_anchors
source_atoms:
- atom-crear-un-documento-ya-fija-sus-anclas-a-documentos-create-document-pinnea-igual-que-save-document-pa
target_kind: test
target_identity: tests/api/test_doc_anchors.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_doc_anchors.py
  tests/api/test_on_write_entering.py
tags:
- system:sldb
- topic:anchors
---

# create-pin test_doc_anchors

## Intent

materializa en tests/api/test_doc_anchors.py el atom atom-crear-un-documento-ya-fija-sus-anclas-a-documentos-create-document-pinnea-igual-que-save-document-pa
