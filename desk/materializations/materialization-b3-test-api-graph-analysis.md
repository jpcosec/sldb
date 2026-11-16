---
sldb:
  by: agent
  at: '2026-11-16T21:04:37Z'
  authority: generated
  via: create_document
id: materialization-b3-test-api-graph-analysis
title: b3 test_api_graph_analysis
source_atoms:
- atom-graph-path-con-explain-devuelve-por-cada-tramo-las-aristas-que-lo-justifican-y-su-procedencia
target_kind: test
target_identity: tests/api/test_api_graph_analysis.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_graph_analysis.py
tags:
- system:sldb
- topic:graph
---

# b3 test_api_graph_analysis

## Intent

materializa en tests/api/test_api_graph_analysis.py el atom atom-graph-path-con-explain-devuelve-por-cada-tramo-las-aristas-que-lo-justifican-y-su-procedencia
