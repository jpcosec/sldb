---
sldb:
  by: agent
  at: '2026-11-17T08:28:18Z'
  authority: generated
  via: create_document
id: materialization-k3-c2-test-treesitter-agreement
title: k3-c2 test_treesitter_agreement
source_atoms:
- atom-los-facts-de-python-traen-bases-decoradores-llamadas-y-asignaciones-genéricas-que-specir-interpreta
target_kind: test
target_identity: tests/selfdoc/test_treesitter_agreement.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# k3-c2 test_treesitter_agreement

## Intent

materializa en tests/selfdoc/test_treesitter_agreement.py el atom atom-los-facts-de-python-traen-bases-decoradores-llamadas-y-asignaciones-genéricas-que-specir-interpreta
