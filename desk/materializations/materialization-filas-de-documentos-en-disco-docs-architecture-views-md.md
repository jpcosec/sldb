---
sldb:
  by: agent
  at: '2026-11-19T16:57:05Z'
  authority: generated
  via: create_document
id: materialization-filas-de-documentos-en-disco-docs-architecture-views-md
title: filas de documentos en disco docs-architecture-views-md
source_atoms:
- atom-select-documents-guarda-en-disco-las-filas-de-documentos-para-que-una-vista-no-reparsee-los-shards-e
target_kind: docs
target_identity: docs/architecture/views.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_select_documents_disk.py
tags:
- system:sldb
- topic:views
---

# filas de documentos en disco docs-architecture-views-md

## Intent

materializa en docs/architecture/views.md el atom atom-select-documents-guarda-en-disco-las-filas-de-documentos-para-que-una-vista-no-reparsee-los-shards-e
