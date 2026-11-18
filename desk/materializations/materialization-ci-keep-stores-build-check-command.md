---
sldb:
  by: agent
  at: '2026-11-18T08:08:31Z'
  authority: generated
  via: create_document
id: materialization-ci-keep-stores-build-check-command
title: ci-keep stores_build_check_command
source_atoms:
- atom-stores-build-check-keep-dir-conserva-la-copia-verificada-y-el-job-store-del-ci-construye-el-store-un
target_kind: code
target_identity: src/sldb/cli/commands/stores_build_check_command.py
validation:
- TMPDIR=/dev/shm PYTHONPATH=src python -m pytest -q -p no:cacheprovider tests/store/test_stores_build.py
tags:
- system:sldb
- topic:ci
---

# ci-keep stores_build_check_command

## Intent

materializa en src/sldb/cli/commands/stores_build_check_command.py el atom atom-stores-build-check-keep-dir-conserva-la-copia-verificada-y-el-job-store-del-ci-construye-el-store-un
