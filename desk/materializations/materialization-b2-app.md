---
sldb:
  by: agent
  at: '2026-11-16T21:30:59Z'
  authority: generated
  via: create_document
id: materialization-b2-app
title: b2 App
source_atoms:
- atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
target_kind: test
target_identity: tests/fixtures/treesitter/frontend/src/App.tsx
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
  tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# b2 App

## Intent

materializa en tests/fixtures/treesitter/frontend/src/App.tsx el atom atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
