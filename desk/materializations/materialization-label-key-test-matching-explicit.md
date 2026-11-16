---
sldb:
  by: agent
  at: '2026-11-16T09:39:07Z'
  authority: generated
  via: create_document
id: materialization-label-key-test-matching-explicit
title: label-key test_matching_explicit
source_atoms:
- atom-label-key-de-sldb-api-matching-normaliza-igual-que-normkey-del-catálogo-el-guion-bajo-separa-palabra
target_kind: test
target_identity: tests/matching/test_matching_explicit.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/matching/
tags:
- system:sldb
- topic:matching
---

# label-key test_matching_explicit

## Intent

materializa en tests/matching/test_matching_explicit.py el atom atom-label-key-de-sldb-api-matching-normaliza-igual-que-normkey-del-catálogo-el-guion-bajo-separa-palabra
