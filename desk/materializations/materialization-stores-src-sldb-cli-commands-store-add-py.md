---
sldb:
  by: agent
  at: '2026-11-20T17:35:48Z'
  authority: generated
  via: create_document
id: materialization-stores-src-sldb-cli-commands-store-add-py
title: stores src-sldb-cli-commands-store_add-py
source_atoms:
- atom-una-operación-de-sldb-se-ancla-al-store-más-cercano-no-al-directorio-desde-donde-se-corre
target_kind: code
target_identity: src/sldb/cli/commands/store_add.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_api_stores.py
tags:
- system:sldb
- topic:stores
---

# stores src-sldb-cli-commands-store_add-py

## Intent

materializa en src/sldb/cli/commands/store_add.py el atom atom-una-operación-de-sldb-se-ancla-al-store-más-cercano-no-al-directorio-desde-donde-se-corre
