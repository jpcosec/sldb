---
sldb:
  by: agent
  at: '2026-11-16T20:15:35Z'
  authority: generated
  via: create_document
id: materialization-leak-test-views-linked
title: leak test_views_linked
source_atoms:
- atom-list-views-no-compone-el-índice-federado-y-compose-edge-index-compone-una-sola-vez-por-clave
target_kind: test
target_identity: tests/api/test_views_linked.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_views_linked.py
  tests/store/test_shard_cache_copies.py
tags:
- system:sldb
- topic:serve
---

# leak test_views_linked

## Intent

materializa en tests/api/test_views_linked.py el atom atom-list-views-no-compone-el-índice-federado-y-compose-edge-index-compone-una-sola-vez-por-clave
