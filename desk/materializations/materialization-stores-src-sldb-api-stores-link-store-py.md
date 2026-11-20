---
sldb:
  by: agent
  at: '2026-11-20T17:35:18Z'
  authority: generated
  via: create_document
id: materialization-stores-src-sldb-api-stores-link-store-py
title: stores src-sldb-api-stores-link_store-py
source_atoms:
- atom-una-operación-de-sldb-se-ancla-al-store-más-cercano-no-al-directorio-desde-donde-se-corre
target_kind: code
target_identity: src/sldb/api/stores/link_store.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_api_stores.py
tags:
- system:sldb
- topic:stores
---

# stores src-sldb-api-stores-link_store-py

## Intent

materializa en src/sldb/api/stores/link_store.py el atom atom-una-operación-de-sldb-se-ancla-al-store-más-cercano-no-al-directorio-desde-donde-se-corre
