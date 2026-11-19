---
sldb:
  by: agent
  at: '2026-11-19T12:11:37Z'
  authority: generated
  via: create_document
id: materialization-directorio-declarado-declared-target-nodes
title: directorio declarado declared_target_nodes
source_atoms:
- atom-un-directorio-existente-declarado-como-target-de-una-materializacion-es-un-nodo-del-grafo-con-o-sin
target_kind: code
target_identity: src/sldb/api/edges/project_graph/declared_target_nodes.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_project_graph.py
tags:
- system:sldb
- topic:graph
---

# directorio declarado declared_target_nodes

## Intent

materializa en src/sldb/api/edges/project_graph/declared_target_nodes.py el atom atom-un-directorio-existente-declarado-como-target-de-una-materializacion-es-un-nodo-del-grafo-con-o-sin
