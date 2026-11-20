---
sldb:
  by: agent
  at: '2026-11-20T10:14:34Z'
  authority: generated
  via: create_document
id: materialization-stores-src-sldb-api-stores-ensure-merge-driver-py
title: stores src-sldb-api-stores-ensure_merge_driver-py
source_atoms:
- atom-los-comandos-cli-de-stores-instalan-solos-el-merge-driver-de-sldb-y-stores-check-avisa-si-falta
target_kind: code
target_identity: src/sldb/api/stores/ensure_merge_driver.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/store/test_merge_driver_auto_install.py
tags:
- system:sldb
- topic:stores
---

# stores src-sldb-api-stores-ensure_merge_driver-py

## Intent

materializa en src/sldb/api/stores/ensure_merge_driver.py el atom atom-los-comandos-cli-de-stores-instalan-solos-el-merge-driver-de-sldb-y-stores-check-avisa-si-falta
