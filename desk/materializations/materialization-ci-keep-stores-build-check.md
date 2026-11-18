---
sldb:
  by: agent
  at: '2026-11-18T08:07:38Z'
  authority: generated
  via: create_document
id: materialization-ci-keep-stores-build-check
title: ci-keep stores_build_check
source_atoms:
- atom-stores-build-check-keep-dir-conserva-la-copia-verificada-y-el-job-store-del-ci-construye-el-store-un
target_kind: code
target_identity: src/sldb/cli/commands/stores_build_check.py
validation:
- TMPDIR=/dev/shm PYTHONPATH=src python -m pytest -q -p no:cacheprovider tests/store/test_stores_build.py
tags:
- system:sldb
- topic:ci
---

# ci-keep stores_build_check

## Intent

materializa en src/sldb/cli/commands/stores_build_check.py el atom atom-stores-build-check-keep-dir-conserva-la-copia-verificada-y-el-job-store-del-ci-construye-el-store-un
