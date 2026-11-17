---
sldb:
  by: agent
  at: '2026-11-17T01:20:32Z'
  authority: generated
  via: create_document
id: materialization-k1-test-anchors
title: k1 test_anchors
source_atoms:
- atom-sldb-api-code-code-facts-es-la-api-pública-de-los-facts-de-código
target_kind: test
target_identity: tests/api/test_anchors.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
tags:
- system:sldb
- topic:code
---

# k1 test_anchors

## Intent

materializa en tests/api/test_anchors.py el atom atom-sldb-api-code-code-facts-es-la-api-pública-de-los-facts-de-código
