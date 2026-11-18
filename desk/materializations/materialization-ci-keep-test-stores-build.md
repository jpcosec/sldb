---
sldb:
  by: agent
  at: '2026-11-18T08:10:07Z'
  authority: generated
  via: create_document
id: materialization-ci-keep-test-stores-build
title: ci-keep test_stores_build
source_atoms:
- atom-stores-build-check-keep-dir-conserva-la-copia-verificada-y-el-job-store-del-ci-construye-el-store-un
target_kind: test
target_identity: tests/store/test_stores_build.py
validation:
- TMPDIR=/dev/shm PYTHONPATH=src python -m pytest -q -p no:cacheprovider tests/store/test_stores_build.py
tags:
- system:sldb
- topic:ci
---

# ci-keep test_stores_build

## Intent

materializa en tests/store/test_stores_build.py el atom atom-stores-build-check-keep-dir-conserva-la-copia-verificada-y-el-job-store-del-ci-construye-el-store-un
