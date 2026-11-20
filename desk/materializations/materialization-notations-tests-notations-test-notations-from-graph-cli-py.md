---
sldb:
  by: agent
  at: '2026-11-20T16:04:52Z'
  authority: generated
  via: create_document
id: materialization-notations-tests-notations-test-notations-from-graph-cli-py
title: notations tests-notations-test_notations_from_graph_cli-py
source_atoms:
- atom-sldb-notations-from-graph-elige-el-campo-del-label-y-el-que-da-kind-o-estilo
target_kind: test
target_identity: tests/notations/test_notations_from_graph_cli.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/notations/test_notations_from_graph_cli.py
tags:
- system:sldb
- topic:notations
---

# notations tests-notations-test_notations_from_graph_cli-py

## Intent

materializa en tests/notations/test_notations_from_graph_cli.py el atom atom-sldb-notations-from-graph-elige-el-campo-del-label-y-el-que-da-kind-o-estilo
