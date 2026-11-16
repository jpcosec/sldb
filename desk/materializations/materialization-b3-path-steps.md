---
sldb:
  by: agent
  at: '2026-11-16T20:58:13Z'
  authority: generated
  via: create_document
id: materialization-b3-path-steps
title: b3 path_steps
source_atoms:
- atom-graph-path-con-explain-devuelve-por-cada-tramo-las-aristas-que-lo-justifican-y-su-procedencia
target_kind: code
target_identity: src/sldb/store/graph/analysis/path_steps.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_graph_analysis.py
tags:
- system:sldb
- topic:graph
---

# b3 path_steps

## Intent

materializa en src/sldb/store/graph/analysis/path_steps.py el atom atom-graph-path-con-explain-devuelve-por-cada-tramo-las-aristas-que-lo-justifican-y-su-procedencia
