---
sldb:
  by: agent
  at: '2026-11-16T09:38:45Z'
  authority: generated
  via: create_document
id: materialization-label-key-atom-keys
title: label-key atom_keys
source_atoms:
- atom-label-key-de-sldb-api-matching-normaliza-igual-que-normkey-del-catálogo-el-guion-bajo-separa-palabra
target_kind: code
target_identity: src/sldb/api/matching/atom_keys.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/matching/
tags:
- system:sldb
- topic:matching
---

# label-key atom_keys

## Intent

materializa en src/sldb/api/matching/atom_keys.py el atom atom-label-key-de-sldb-api-matching-normaliza-igual-que-normkey-del-catálogo-el-guion-bajo-separa-palabra
