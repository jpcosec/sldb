---
sldb:
  by: agent
  at: '2026-11-17T01:18:35Z'
  authority: generated
  via: create_document
id: materialization-k1-code-facts
title: k1 code_facts
source_atoms:
- atom-sldb-api-code-code-facts-es-la-api-pública-de-los-facts-de-código
target_kind: code
target_identity: src/sldb/api/code/code_facts.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
tags:
- system:sldb
- topic:code
---

# k1 code_facts

## Intent

materializa en src/sldb/api/code/code_facts.py el atom atom-sldb-api-code-code-facts-es-la-api-pública-de-los-facts-de-código
