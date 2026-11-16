---
sldb:
  by: agent
  at: '2026-11-16T21:29:18Z'
  authority: generated
  via: create_document
id: materialization-b2-code-ref
title: b2 code_ref
source_atoms:
- atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
target_kind: code
target_identity: src/sldb/models/code_ref.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
  tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# b2 code_ref

## Intent

materializa en src/sldb/models/code_ref.py el atom atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
