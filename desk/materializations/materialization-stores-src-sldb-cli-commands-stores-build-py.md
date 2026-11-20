---
sldb:
  by: agent
  at: '2026-11-20T10:15:59Z'
  authority: generated
  via: create_document
id: materialization-stores-src-sldb-cli-commands-stores-build-py
title: stores src-sldb-cli-commands-stores_build-py
source_atoms:
- atom-los-comandos-cli-de-stores-instalan-solos-el-merge-driver-de-sldb-y-stores-check-avisa-si-falta
target_kind: code
target_identity: src/sldb/cli/commands/stores_build.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/store/test_merge_driver_auto_install.py
tags:
- system:sldb
- topic:stores
---

# stores src-sldb-cli-commands-stores_build-py

## Intent

materializa en src/sldb/cli/commands/stores_build.py el atom atom-los-comandos-cli-de-stores-instalan-solos-el-merge-driver-de-sldb-y-stores-check-avisa-si-falta
