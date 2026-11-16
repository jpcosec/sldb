---
sldb:
  by: agent
  at: '2026-11-16T10:24:46Z'
  authority: generated
  via: create_document
id: materialization-read-store-test-api-stores
title: read-store test_api_stores
source_atoms:
- atom-un-lector-que-no-debe-escribir-abre-el-store-con-read-store-que-no-migra-y-rechaza-un-store-no-prepa
target_kind: test
target_identity: tests/api/test_api_stores.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py
tags:
- system:sldb
- topic:store
---

# read-store test_api_stores

## Intent

materializa en tests/api/test_api_stores.py el atom atom-un-lector-que-no-debe-escribir-abre-el-store-con-read-store-que-no-migra-y-rechaza-un-store-no-prepa
