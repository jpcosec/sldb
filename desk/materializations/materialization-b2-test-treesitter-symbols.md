---
sldb:
  by: agent
  at: '2026-11-16T21:30:34Z'
  authority: generated
  via: create_document
id: materialization-b2-test-treesitter-symbols
title: b2 test_treesitter_symbols
source_atoms:
- atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
target_kind: test
target_identity: tests/selfdoc/test_treesitter_symbols.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
  tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# b2 test_treesitter_symbols

## Intent

materializa en tests/selfdoc/test_treesitter_symbols.py el atom atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
