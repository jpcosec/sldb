---
sldb:
  by: agent
  at: '2026-11-17T08:30:22Z'
  authority: generated
  via: create_document
id: materialization-k3-c2-readers
title: k3-c2 readers
source_atoms:
- atom-los-facts-de-python-traen-bases-decoradores-llamadas-y-asignaciones-genéricas-que-specir-interpreta
target_kind: code
target_identity: src/sldb/code/readers.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# k3-c2 readers

## Intent

materializa en src/sldb/code/readers.py el atom atom-los-facts-de-python-traen-bases-decoradores-llamadas-y-asignaciones-genéricas-que-specir-interpreta
