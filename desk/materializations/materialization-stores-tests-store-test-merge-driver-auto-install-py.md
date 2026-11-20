---
sldb:
  by: agent
  at: '2026-11-20T10:17:23Z'
  authority: generated
  via: create_document
id: materialization-stores-tests-store-test-merge-driver-auto-install-py
title: stores tests-store-test_merge_driver_auto_install-py
source_atoms:
- atom-los-comandos-cli-de-stores-instalan-solos-el-merge-driver-de-sldb-y-stores-check-avisa-si-falta
target_kind: test
target_identity: tests/store/test_merge_driver_auto_install.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/store/test_merge_driver_auto_install.py
tags:
- system:sldb
- topic:stores
---

# stores tests-store-test_merge_driver_auto_install-py

## Intent

materializa en tests/store/test_merge_driver_auto_install.py el atom atom-los-comandos-cli-de-stores-instalan-solos-el-merge-driver-de-sldb-y-stores-check-avisa-si-falta
