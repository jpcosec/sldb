---
sldb:
  by: agent
  at: '2026-11-17T13:40:43Z'
  authority: generated
  via: create_document
id: materialization-k4-nc-postform
title: k4-nc PostForm
source_atoms:
- atom-los-facts-de-ts-y-js-traen-sus-llamadas-con-nombre-canónico-url-literal-y-handlers-jsx
target_kind: test
target_identity: tests/fixtures/treesitter/frontend/src/PostForm.tsx
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# k4-nc PostForm

## Intent

materializa en tests/fixtures/treesitter/frontend/src/PostForm.tsx el atom atom-los-facts-de-ts-y-js-traen-sus-llamadas-con-nombre-canónico-url-literal-y-handlers-jsx
