---
sldb:
  by: agent
  at: '2026-11-20T17:34:50Z'
  authority: generated
  via: create_document
id: materialization-stores-docs-architecture-store-declaration-md
title: stores docs-architecture-store-declaration-md
source_atoms:
- atom-una-operación-de-sldb-se-ancla-al-store-más-cercano-no-al-directorio-desde-donde-se-corre
target_kind: docs
target_identity: docs/architecture/store-declaration.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_api_stores.py
tags:
- system:sldb
- topic:stores
---

# stores docs-architecture-store-declaration-md

## Intent

materializa en docs/architecture/store-declaration.md el atom atom-una-operación-de-sldb-se-ancla-al-store-más-cercano-no-al-directorio-desde-donde-se-corre
