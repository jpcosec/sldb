---
sldb:
  by: agent
  at: '2026-11-18T08:09:34Z'
  authority: generated
  via: create_document
id: materialization-ci-keep-parser-stores
title: ci-keep parser stores
source_atoms:
- atom-stores-build-check-keep-dir-conserva-la-copia-verificada-y-el-job-store-del-ci-construye-el-store-un
target_kind: code
target_identity: src/sldb/cli/parsers/stores.py
validation:
- TMPDIR=/dev/shm PYTHONPATH=src python -m pytest -q -p no:cacheprovider tests/store/test_stores_build.py
tags:
- system:sldb
- topic:ci
---

# ci-keep parser stores

## Intent

materializa en src/sldb/cli/parsers/stores.py el atom atom-stores-build-check-keep-dir-conserva-la-copia-verificada-y-el-job-store-del-ci-construye-el-store-un
