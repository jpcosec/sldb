---
id: materialization-gd21-project-graph-store-project-graph
title: gd21 project_graph store_project_graph
source_atoms:
- atom-el-grafo-de-un-proyecto-se-declara-en-store-yaml-y-sldb-lo-sirve
target_kind: code
target_identity: src/sldb/api/edges/project_graph/store_project_graph.py
validation:
- pytest -q tests/api/test_project_graph.py tests/api/test_project_graph_config.py
tags:
- system:sldb
- topic:project-graph
---

# gd21 project_graph store_project_graph

## Intent

materializa atom-el-grafo-de-un-proyecto-se-declara-en-store-yaml-y-sldb-lo-sirve en src/sldb/api/edges/project_graph/store_project_graph.py
