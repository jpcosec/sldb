---
sldb:
  by: agent
  at: '2026-11-16T10:25:07Z'
  authority: generated
  via: create_document
id: materialization-read-store-store-declaration
title: read-store store-declaration
source_atoms:
- atom-un-lector-que-no-debe-escribir-abre-el-store-con-read-store-que-no-migra-y-rechaza-un-store-no-prepa
target_kind: doc
target_identity: docs/architecture/store-declaration.md
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py
tags:
- system:sldb
- topic:store
---

# read-store store-declaration

## Intent

materializa en docs/architecture/store-declaration.md el atom atom-un-lector-que-no-debe-escribir-abre-el-store-con-read-store-que-no-migra-y-rechaza-un-store-no-prepa
