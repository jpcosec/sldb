---
sldb:
  by: agent
  at: '2026-11-20T02:57:26Z'
  authority: generated
  via: create_document
id: materialization-cache-ve-reescritura-src-sldb-store-layout-py
title: caché ve reescritura src-sldb-store-layout-py
source_atoms:
- atom-las-caches-de-disco-de-sldb-ven-una-reescritura-in-place-de-un-documento-y-stores-build-las-invalida
target_kind: code
target_identity: src/sldb/store/layout.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_select_documents_disk.py
tags:
- system:sldb
- topic:cache
---

# caché ve reescritura src-sldb-store-layout-py

## Intent

materializa en src/sldb/store/layout.py el atom atom-las-caches-de-disco-de-sldb-ven-una-reescritura-in-place-de-un-documento-y-stores-build-las-invalida
