---
sldb:
  by: agent
  at: '2026-11-16T21:03:51Z'
  authority: generated
  via: create_document
id: materialization-b3-graph-routes
title: b3 graph_routes
source_atoms:
- atom-graph-path-con-explain-devuelve-por-cada-tramo-las-aristas-que-lo-justifican-y-su-procedencia
target_kind: code
target_identity: src/sldb/cli/serve/graph_routes.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_graph_analysis.py
tags:
- system:sldb
- topic:graph
---

# b3 graph_routes

## Intent

materializa en src/sldb/cli/serve/graph_routes.py el atom atom-graph-path-con-explain-devuelve-por-cada-tramo-las-aristas-que-lo-justifican-y-su-procedencia
