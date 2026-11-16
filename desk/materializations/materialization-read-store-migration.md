---
sldb:
  by: agent
  at: '2026-11-16T10:28:40Z'
  authority: generated
  via: create_document
id: materialization-read-store-migration
title: read-store migration
source_atoms:
- atom-un-lector-que-no-debe-escribir-abre-el-store-con-read-store-que-no-migra-y-rechaza-un-store-no-prepa
target_kind: code
target_identity: src/sldb/store/migration.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py
tags:
- system:sldb
- topic:store
---

# read-store migration

## Intent

materializa en src/sldb/store/migration.py la comprobación de layout canónico (_already_canonical) que read_store y store_is_prepared usan sin migrar
