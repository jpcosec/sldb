---
sldb:
  by: agent
  at: '2026-11-20T10:15:03Z'
  authority: generated
  via: create_document
id: materialization-stores-src-sldb-api-stores-store-surroundings-py
title: stores src-sldb-api-stores-store_surroundings-py
source_atoms:
- atom-los-comandos-cli-de-stores-instalan-solos-el-merge-driver-de-sldb-y-stores-check-avisa-si-falta
target_kind: code
target_identity: src/sldb/api/stores/store_surroundings.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/store/test_merge_driver_auto_install.py
tags:
- system:sldb
- topic:stores
---

# stores src-sldb-api-stores-store_surroundings-py

## Intent

materializa en src/sldb/api/stores/store_surroundings.py el atom atom-los-comandos-cli-de-stores-instalan-solos-el-merge-driver-de-sldb-y-stores-check-avisa-si-falta
