---
sldb:
  by: agent
  at: '2026-11-17T01:19:03Z'
  authority: generated
  via: create_document
id: materialization-k1-requested-files
title: k1 requested_files
source_atoms:
- atom-sldb-api-code-code-facts-es-la-api-pública-de-los-facts-de-código
target_kind: code
target_identity: src/sldb/api/code/requested_files.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
tags:
- system:sldb
- topic:code
---

# k1 requested_files

## Intent

materializa en src/sldb/api/code/requested_files.py el atom atom-sldb-api-code-code-facts-es-la-api-pública-de-los-facts-de-código
