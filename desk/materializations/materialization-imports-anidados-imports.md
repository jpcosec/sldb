---
sldb:
  by: agent
  at: '2026-11-16T09:22:17Z'
  authority: generated
  via: create_document
id: materialization-imports-anidados-imports
title: imports anidados imports
source_atoms:
- atom-los-imports-anidados-de-un-módulo-python-son-un-hecho-aparte-de-los-de-nivel-superior-y-el-spec-de-c
target_kind: code
target_identity: src/sldb/code/imports.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_python.py
  tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code-facts
---

# imports anidados imports

## Intent

materializa en src/sldb/code/imports.py que los imports anidados son un attr aparte y que el spec de componentes los dibuja
