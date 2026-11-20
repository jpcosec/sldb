---
sldb:
  by: agent
  at: '2026-11-20T16:03:26Z'
  authority: generated
  via: create_document
id: materialization-notations-src-sldb-api-notations-component-spec-graph-py
title: notations src-sldb-api-notations-component_spec_graph-py
source_atoms:
- atom-sldb-notations-from-graph-elige-el-campo-del-label-y-el-que-da-kind-o-estilo
target_kind: code
target_identity: src/sldb/api/notations/component_spec_graph.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/notations/test_notations_from_graph_cli.py
tags:
- system:sldb
- topic:notations
---

# notations src-sldb-api-notations-component_spec_graph-py

## Intent

materializa en src/sldb/api/notations/component_spec_graph.py el atom atom-sldb-notations-from-graph-elige-el-campo-del-label-y-el-que-da-kind-o-estilo
