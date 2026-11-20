---
sldb:
  by: agent
  at: '2026-11-20T10:15:31Z'
  authority: generated
  via: create_document
id: materialization-stores-src-sldb-cli-commands-store-init-py
title: stores src-sldb-cli-commands-store_init-py
source_atoms:
- atom-los-comandos-cli-de-stores-instalan-solos-el-merge-driver-de-sldb-y-stores-check-avisa-si-falta
target_kind: code
target_identity: src/sldb/cli/commands/store_init.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/store/test_merge_driver_auto_install.py
tags:
- system:sldb
- topic:stores
---

# stores src-sldb-cli-commands-store_init-py

## Intent

materializa en src/sldb/cli/commands/store_init.py el atom atom-los-comandos-cli-de-stores-instalan-solos-el-merge-driver-de-sldb-y-stores-check-avisa-si-falta
