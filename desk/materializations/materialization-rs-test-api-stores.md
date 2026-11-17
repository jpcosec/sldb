---
sldb:
  by: agent
  at: '2026-11-17T14:10:07Z'
  authority: generated
  via: create_document
id: materialization-rs-test-api-stores
title: rs test_api_stores
source_atoms:
- atom-read-store-dice-store-not-found-si-el-sldb-no-existe-y-store-not-prepared-si-le-falta-el-índice
target_kind: test
target_identity: tests/api/test_api_stores.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py
tags:
- system:sldb
- topic:store
---

# rs test_api_stores

## Intent

materializa en tests/api/test_api_stores.py el atom atom-read-store-dice-store-not-found-si-el-sldb-no-existe-y-store-not-prepared-si-le-falta-el-índice
