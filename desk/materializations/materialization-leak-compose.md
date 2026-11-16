---
sldb:
  by: agent
  at: '2026-11-16T20:14:15Z'
  authority: generated
  via: create_document
id: materialization-leak-compose
title: leak compose
source_atoms:
- atom-list-views-no-compone-el-índice-federado-y-compose-edge-index-compone-una-sola-vez-por-clave
target_kind: code
target_identity: src/sldb/store/edge_index/compose.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_views_linked.py
  tests/store/test_shard_cache_copies.py
tags:
- system:sldb
- topic:serve
---

# leak compose

## Intent

materializa en src/sldb/store/edge_index/compose.py el atom atom-list-views-no-compone-el-índice-federado-y-compose-edge-index-compone-una-sola-vez-por-clave
