---
id: materialization-gd21-api-test-project-graph
title: gd21 api test_project_graph
source_atoms:
- atom-el-grafo-de-un-proyecto-se-declara-en-store-yaml-y-sldb-lo-sirve
target_kind: test
target_identity: tests/api/test_project_graph.py
validation:
- pytest -q tests/api/test_project_graph.py
tags:
- system:sldb
- topic:project-graph
---

# gd21 api test_project_graph

## Intent

materializa atom-el-grafo-de-un-proyecto-se-declara-en-store-yaml-y-sldb-lo-sirve en tests/api/test_project_graph.py
