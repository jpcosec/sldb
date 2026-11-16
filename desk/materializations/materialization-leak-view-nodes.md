---
sldb:
  by: agent
  at: '2026-11-16T20:13:30Z'
  authority: generated
  via: create_document
id: materialization-leak-view-nodes
title: leak view_nodes
source_atoms:
- atom-list-views-no-compone-el-índice-federado-y-compose-edge-index-compone-una-sola-vez-por-clave
target_kind: code
target_identity: src/sldb/api/views/view_nodes.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_views_linked.py
  tests/store/test_shard_cache_copies.py
tags:
- system:sldb
- topic:serve
---

# leak view_nodes

## Intent

materializa en src/sldb/api/views/view_nodes.py el atom atom-list-views-no-compone-el-índice-federado-y-compose-edge-index-compone-una-sola-vez-por-clave
