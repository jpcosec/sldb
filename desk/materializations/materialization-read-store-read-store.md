---
sldb:
  by: agent
  at: '2026-11-16T10:23:42Z'
  authority: generated
  via: create_document
id: materialization-read-store-read-store
title: read-store read_store
source_atoms:
- atom-un-lector-que-no-debe-escribir-abre-el-store-con-read-store-que-no-migra-y-rechaza-un-store-no-prepa
target_kind: code
target_identity: src/sldb/api/stores/read_store.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py
tags:
- system:sldb
- topic:store
---

# read-store read_store

## Intent

materializa en src/sldb/api/stores/read_store.py el atom atom-un-lector-que-no-debe-escribir-abre-el-store-con-read-store-que-no-migra-y-rechaza-un-store-no-prepa
