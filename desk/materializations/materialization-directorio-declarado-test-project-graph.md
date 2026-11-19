---
sldb:
  by: agent
  at: '2026-11-19T12:12:33Z'
  authority: generated
  via: create_document
id: materialization-directorio-declarado-test-project-graph
title: directorio declarado test_project_graph
source_atoms:
- atom-un-directorio-existente-declarado-como-target-de-una-materializacion-es-un-nodo-del-grafo-con-o-sin
target_kind: test
target_identity: tests/api/test_project_graph.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_project_graph.py
tags:
- system:sldb
- topic:graph
---

# directorio declarado test_project_graph

## Intent

materializa en tests/api/test_project_graph.py el atom atom-un-directorio-existente-declarado-como-target-de-una-materializacion-es-un-nodo-del-grafo-con-o-sin
