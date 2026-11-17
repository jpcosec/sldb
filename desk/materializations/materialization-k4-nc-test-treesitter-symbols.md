---
sldb:
  by: agent
  at: '2026-11-17T13:41:12Z'
  authority: generated
  via: create_document
id: materialization-k4-nc-test-treesitter-symbols
title: k4-nc test_treesitter_symbols
source_atoms:
- atom-los-facts-de-ts-y-js-traen-sus-llamadas-con-nombre-canónico-url-literal-y-handlers-jsx
target_kind: test
target_identity: tests/selfdoc/test_treesitter_symbols.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# k4-nc test_treesitter_symbols

## Intent

materializa en tests/selfdoc/test_treesitter_symbols.py el atom atom-los-facts-de-ts-y-js-traen-sus-llamadas-con-nombre-canónico-url-literal-y-handlers-jsx
