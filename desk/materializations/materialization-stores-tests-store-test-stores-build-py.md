---
sldb:
  by: agent
  at: '2026-11-20T17:37:13Z'
  authority: generated
  via: create_document
id: materialization-stores-tests-store-test-stores-build-py
title: stores tests-store-test_stores_build-py
source_atoms:
- atom-una-operación-de-sldb-se-ancla-al-store-más-cercano-no-al-directorio-desde-donde-se-corre
target_kind: test
target_identity: tests/store/test_stores_build.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_api_stores.py
tags:
- system:sldb
- topic:stores
---

# stores tests-store-test_stores_build-py

## Intent

materializa en tests/store/test_stores_build.py el atom atom-una-operación-de-sldb-se-ancla-al-store-más-cercano-no-al-directorio-desde-donde-se-corre
