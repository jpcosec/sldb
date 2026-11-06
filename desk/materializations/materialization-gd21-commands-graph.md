---
id: materialization-gd21-commands-graph
title: gd21 commands graph
source_atoms:
- atom-el-grafo-de-un-proyecto-se-declara-en-store-yaml-y-sldb-lo-sirve
target_kind: code
target_identity: src/sldb/cli/commands/graph.py
validation:
- pytest -q tests/api/test_project_graph.py tests/api/test_project_graph_config.py
tags:
- system:sldb
- topic:project-graph
---

# gd21 commands graph

## Intent

materializa atom-el-grafo-de-un-proyecto-se-declara-en-store-yaml-y-sldb-lo-sirve en src/sldb/cli/commands/graph.py
