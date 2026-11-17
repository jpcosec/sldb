---
sldb:
  by: agent
  at: '2026-11-17T14:09:35Z'
  authority: generated
  via: create_document
id: materialization-rs-read-store
title: rs read_store
source_atoms:
- atom-read-store-dice-store-not-found-si-el-sldb-no-existe-y-store-not-prepared-si-le-falta-el-índice
target_kind: code
target_identity: src/sldb/api/stores/read_store.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py
tags:
- system:sldb
- topic:store
---

# rs read_store

## Intent

materializa en src/sldb/api/stores/read_store.py el atom atom-read-store-dice-store-not-found-si-el-sldb-no-existe-y-store-not-prepared-si-le-falta-el-índice
