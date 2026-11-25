---
sldb:
  by: agent
  at: '2026-11-25T22:29:55Z'
  authority: generated
  via: create_document
id: materialization-layout-partition-lanes-tests-notations-test-layout-partition-lanes-py
title: layout-partition-lanes tests-notations-test_layout_partition_lanes-py
source_atoms:
- atom-el-layout-de-una-notationdoc-acepta-partition-lanes-con-by
target_kind: test
target_identity: tests/notations/test_layout_partition_lanes.py
validation:
- pytest -q tests/notations/test_layout_partition_lanes.py
tags:
- system:sldb
- topic:layout-partition-lanes
---

# layout-partition-lanes tests-notations-test_layout_partition_lanes-py

## Intent

materializa en tests/notations/test_layout_partition_lanes.py el atom atom-el-layout-de-una-notationdoc-acepta-partition-lanes-con-by
