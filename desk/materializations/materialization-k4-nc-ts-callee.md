---
sldb:
  by: agent
  at: '2026-11-17T13:38:32Z'
  authority: generated
  via: create_document
id: materialization-k4-nc-ts-callee
title: k4-nc ts_callee
source_atoms:
- atom-los-facts-de-ts-y-js-traen-sus-llamadas-con-nombre-canónico-url-literal-y-handlers-jsx
target_kind: code
target_identity: src/sldb/code/ts_callee.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# k4-nc ts_callee

## Intent

materializa en src/sldb/code/ts_callee.py el atom atom-los-facts-de-ts-y-js-traen-sus-llamadas-con-nombre-canónico-url-literal-y-handlers-jsx
