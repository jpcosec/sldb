---
sldb:
  by: agent
  at: '2026-11-16T21:29:43Z'
  authority: generated
  via: create_document
id: materialization-b2-record-anchor
title: b2 record_anchor
source_atoms:
- atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
target_kind: code
target_identity: src/sldb/api/anchors/record_anchor.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
  tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# b2 record_anchor

## Intent

materializa en src/sldb/api/anchors/record_anchor.py el atom atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
