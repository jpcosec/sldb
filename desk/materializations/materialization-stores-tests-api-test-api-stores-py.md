---
sldb:
  by: agent
  at: '2026-11-20T17:36:44Z'
  authority: generated
  via: create_document
id: materialization-stores-tests-api-test-api-stores-py
title: stores tests-api-test_api_stores-py
source_atoms:
- atom-una-operación-de-sldb-se-ancla-al-store-más-cercano-no-al-directorio-desde-donde-se-corre
target_kind: test
target_identity: tests/api/test_api_stores.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_api_stores.py
tags:
- system:sldb
- topic:stores
---

# stores tests-api-test_api_stores-py

## Intent

materializa en tests/api/test_api_stores.py el atom atom-una-operación-de-sldb-se-ancla-al-store-más-cercano-no-al-directorio-desde-donde-se-corre
