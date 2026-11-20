---
sldb:
  by: agent
  at: '2026-11-20T02:55:59Z'
  authority: generated
  via: create_document
id: materialization-cache-ve-reescritura-src-sldb-api-stores-build-store-py
title: caché ve reescritura src-sldb-api-stores-build_store-py
source_atoms:
- atom-las-caches-de-disco-de-sldb-ven-una-reescritura-in-place-de-un-documento-y-stores-build-las-invalida
target_kind: code
target_identity: src/sldb/api/stores/build_store.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_select_documents_disk.py
tags:
- system:sldb
- topic:cache
---

# caché ve reescritura src-sldb-api-stores-build_store-py

## Intent

materializa en src/sldb/api/stores/build_store.py el atom atom-las-caches-de-disco-de-sldb-ven-una-reescritura-in-place-de-un-documento-y-stores-build-las-invalida
