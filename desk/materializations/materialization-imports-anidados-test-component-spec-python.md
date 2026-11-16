---
sldb:
  by: agent
  at: '2026-11-16T09:23:22Z'
  authority: generated
  via: create_document
id: materialization-imports-anidados-test-component-spec-python
title: imports anidados test_component_spec_python
source_atoms:
- atom-los-imports-anidados-de-un-módulo-python-son-un-hecho-aparte-de-los-de-nivel-superior-y-el-spec-de-c
target_kind: test
target_identity: tests/notations/test_component_spec_python.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_python.py
  tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code-facts
---

# imports anidados test_component_spec_python

## Intent

materializa en tests/notations/test_component_spec_python.py que los imports anidados son un attr aparte y que el spec de componentes los dibuja
