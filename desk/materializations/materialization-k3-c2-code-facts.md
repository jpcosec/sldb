---
sldb:
  by: agent
  at: '2026-11-17T08:27:06Z'
  authority: generated
  via: create_document
id: materialization-k3-c2-code-facts
title: k3-c2 code_facts
source_atoms:
- atom-los-facts-de-python-traen-bases-decoradores-llamadas-y-asignaciones-genéricas-que-specir-interpreta
target_kind: code
target_identity: src/sldb/api/code/code_facts.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# k3-c2 code_facts

## Intent

materializa en src/sldb/api/code/code_facts.py el atom atom-los-facts-de-python-traen-bases-decoradores-llamadas-y-asignaciones-genéricas-que-specir-interpreta
