---
sldb:
  by: agent
  at: '2026-11-16T20:16:02Z'
  authority: generated
  via: create_document
id: materialization-leak-test-shard-cache-copies
title: leak test_shard_cache_copies
source_atoms:
- atom-list-views-no-compone-el-índice-federado-y-compose-edge-index-compone-una-sola-vez-por-clave
target_kind: test
target_identity: tests/store/test_shard_cache_copies.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_views_linked.py
  tests/store/test_shard_cache_copies.py
tags:
- system:sldb
- topic:serve
---

# leak test_shard_cache_copies

## Intent

materializa en tests/store/test_shard_cache_copies.py el atom atom-list-views-no-compone-el-índice-federado-y-compose-edge-index-compone-una-sola-vez-por-clave
