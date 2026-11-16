---
sldb:
  by: agent
  at: '2026-11-16T10:24:03Z'
  authority: generated
  via: create_document
id: materialization-read-store-extract-payload
title: read-store extract_payload
source_atoms:
- atom-un-lector-que-no-debe-escribir-abre-el-store-con-read-store-que-no-migra-y-rechaza-un-store-no-prepa
target_kind: code
target_identity: src/sldb/api/documents/extract_payload.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py
tags:
- system:sldb
- topic:store
---

# read-store extract_payload

## Intent

materializa en src/sldb/api/documents/extract_payload.py el atom atom-un-lector-que-no-debe-escribir-abre-el-store-con-read-store-que-no-migra-y-rechaza-un-store-no-prepa
