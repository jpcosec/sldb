---
sldb:
  by: agent
  at: '2026-11-19T16:59:29Z'
  authority: generated
  via: create_document
id: materialization-filas-de-documentos-en-disco-src-sldb-store-graph-analysis-lazy-networkx-py
title: filas de documentos en disco src-sldb-store-graph-analysis-lazy_networkx-py
source_atoms:
- atom-select-documents-guarda-en-disco-las-filas-de-documentos-para-que-una-vista-no-reparsee-los-shards-e
target_kind: code
target_identity: src/sldb/store/graph/analysis/lazy_networkx.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_select_documents_disk.py
tags:
- system:sldb
- topic:views
---

# filas de documentos en disco src-sldb-store-graph-analysis-lazy_networkx-py

## Intent

materializa en src/sldb/store/graph/analysis/lazy_networkx.py el atom atom-select-documents-guarda-en-disco-las-filas-de-documentos-para-que-una-vista-no-reparsee-los-shards-e
