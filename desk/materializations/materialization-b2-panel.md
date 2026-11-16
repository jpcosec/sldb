---
sldb:
  by: agent
  at: '2026-11-16T21:31:24Z'
  authority: generated
  via: create_document
id: materialization-b2-panel
title: b2 Panel
source_atoms:
- atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
target_kind: test
target_identity: tests/fixtures/treesitter/frontend/src/Panel.jsx
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
  tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# b2 Panel

## Intent

materializa en tests/fixtures/treesitter/frontend/src/Panel.jsx el atom atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
