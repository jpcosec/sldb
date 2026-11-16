---
sldb:
  by: agent
  at: '2026-11-16T21:31:56Z'
  authority: generated
  via: create_document
id: materialization-b2-usetoggle
title: b2 useToggle
source_atoms:
- atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
target_kind: test
target_identity: tests/fixtures/treesitter/frontend/src/useToggle.ts
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
  tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# b2 useToggle

## Intent

materializa en tests/fixtures/treesitter/frontend/src/useToggle.ts el atom atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
