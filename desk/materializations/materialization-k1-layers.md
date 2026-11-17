---
sldb:
  by: agent
  at: '2026-11-17T01:20:03Z'
  authority: generated
  via: create_document
id: materialization-k1-layers
title: k1 layers
source_atoms:
- atom-sldb-api-code-code-facts-es-la-api-pública-de-los-facts-de-código
target_kind: code
target_identity: contracts/layers.toml
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
tags:
- system:sldb
- topic:code
---

# k1 layers

## Intent

materializa en contracts/layers.toml el atom atom-sldb-api-code-code-facts-es-la-api-pública-de-los-facts-de-código
