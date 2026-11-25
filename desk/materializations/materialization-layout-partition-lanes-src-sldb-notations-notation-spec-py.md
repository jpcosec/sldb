---
sldb:
  by: agent
  at: '2026-11-25T22:29:21Z'
  authority: generated
  via: create_document
id: materialization-layout-partition-lanes-src-sldb-notations-notation-spec-py
title: layout-partition-lanes src-sldb-notations-notation_spec-py
source_atoms:
- atom-el-layout-de-una-notationdoc-acepta-partition-lanes-con-by
target_kind: code
target_identity: src/sldb/notations/notation_spec.py
validation:
- pytest -q tests/notations/test_layout_partition_lanes.py
tags:
- system:sldb
- topic:layout-partition-lanes
---

# layout-partition-lanes src-sldb-notations-notation_spec-py

## Intent

materializa en src/sldb/notations/notation_spec.py el atom atom-el-layout-de-una-notationdoc-acepta-partition-lanes-con-by
