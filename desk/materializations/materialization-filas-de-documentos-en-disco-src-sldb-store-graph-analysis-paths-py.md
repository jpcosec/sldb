---
sldb:
  by: agent
  at: '2026-11-19T17:00:57Z'
  authority: generated
  via: create_document
id: materialization-filas-de-documentos-en-disco-src-sldb-store-graph-analysis-paths-py
title: filas de documentos en disco src-sldb-store-graph-analysis-paths-py
source_atoms:
- atom-select-documents-guarda-en-disco-las-filas-de-documentos-para-que-una-vista-no-reparsee-los-shards-e
target_kind: code
target_identity: src/sldb/store/graph/analysis/paths.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_select_documents_disk.py
tags:
- system:sldb
- topic:views
---

# filas de documentos en disco src-sldb-store-graph-analysis-paths-py

## Intent

materializa en src/sldb/store/graph/analysis/paths.py el atom atom-select-documents-guarda-en-disco-las-filas-de-documentos-para-que-una-vista-no-reparsee-los-shards-e
