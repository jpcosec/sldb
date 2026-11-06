---
id: materialization-gd21-project-graph-project-graph-config-mapping
title: gd21 project_graph project_graph_config_mapping
source_atoms:
- atom-el-grafo-de-un-proyecto-se-declara-en-store-yaml-y-sldb-lo-sirve
target_kind: code
target_identity: src/sldb/api/edges/project_graph/project_graph_config_mapping.py
validation:
- pytest -q tests/api/test_project_graph.py tests/api/test_project_graph_config.py
tags:
- system:sldb
- topic:project-graph
---

# gd21 project_graph project_graph_config_mapping

## Intent

materializa atom-el-grafo-de-un-proyecto-se-declara-en-store-yaml-y-sldb-lo-sirve en src/sldb/api/edges/project_graph/project_graph_config_mapping.py
