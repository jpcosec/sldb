---
sldb:
  by: agent
  at: '2026-11-19T16:56:36Z'
  authority: generated
  via: create_document
id: materialization-filas-de-documentos-en-disco-contracts-layers-toml
title: filas de documentos en disco contracts-layers-toml
source_atoms:
- atom-select-documents-guarda-en-disco-las-filas-de-documentos-para-que-una-vista-no-reparsee-los-shards-e
target_kind: config
target_identity: contracts/layers.toml
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_select_documents_disk.py
tags:
- system:sldb
- topic:views
---

# filas de documentos en disco contracts-layers-toml

## Intent

materializa en contracts/layers.toml el atom atom-select-documents-guarda-en-disco-las-filas-de-documentos-para-que-una-vista-no-reparsee-los-shards-e
