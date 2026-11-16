---
sldb:
  by: agent
  at: '2026-11-16T21:02:14Z'
  authority: generated
  via: create_document
id: materialization-b3-graph-analysis-command
title: b3 graph_analysis command
source_atoms:
- atom-graph-path-con-explain-devuelve-por-cada-tramo-las-aristas-que-lo-justifican-y-su-procedencia
target_kind: code
target_identity: src/sldb/cli/commands/graph_analysis.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_graph_analysis.py
tags:
- system:sldb
- topic:graph
---

# b3 graph_analysis command

## Intent

materializa en src/sldb/cli/commands/graph_analysis.py el atom atom-graph-path-con-explain-devuelve-por-cada-tramo-las-aristas-que-lo-justifican-y-su-procedencia
