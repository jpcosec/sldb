---
sldb:
  by: agent
  at: '2026-11-16T21:26:00Z'
  authority: generated
  via: create_document
id: materialization-b2-pyproject
title: b2 pyproject
source_atoms:
- atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
target_kind: code
target_identity: pyproject.toml
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
  tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# b2 pyproject

## Intent

materializa en pyproject.toml el atom atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
