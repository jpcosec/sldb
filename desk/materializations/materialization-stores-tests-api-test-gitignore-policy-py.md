---
sldb:
  by: agent
  at: '2026-11-20T10:16:55Z'
  authority: generated
  via: create_document
id: materialization-stores-tests-api-test-gitignore-policy-py
title: stores tests-api-test_gitignore_policy-py
source_atoms:
- atom-los-comandos-cli-de-stores-instalan-solos-el-merge-driver-de-sldb-y-stores-check-avisa-si-falta
target_kind: test
target_identity: tests/api/test_gitignore_policy.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/store/test_merge_driver_auto_install.py
tags:
- system:sldb
- topic:stores
---

# stores tests-api-test_gitignore_policy-py

## Intent

materializa en tests/api/test_gitignore_policy.py el atom atom-los-comandos-cli-de-stores-instalan-solos-el-merge-driver-de-sldb-y-stores-check-avisa-si-falta
