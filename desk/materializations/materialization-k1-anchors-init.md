---
sldb:
  by: agent
  at: '2026-11-17T01:19:32Z'
  authority: generated
  via: create_document
id: materialization-k1-anchors-init
title: k1 anchors __init__
source_atoms:
- atom-sldb-api-code-code-facts-es-la-api-pública-de-los-facts-de-código
target_kind: code
target_identity: src/sldb/api/anchors/__init__.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
tags:
- system:sldb
- topic:code
---

# k1 anchors __init__

## Intent

materializa en src/sldb/api/anchors/__init__.py el atom atom-sldb-api-code-code-facts-es-la-api-pública-de-los-facts-de-código
