---
sldb:
  by: agent
  at: '2026-11-17T08:33:54Z'
  authority: generated
  via: create_document
id: materialization-k3-c2-blogsite-init
title: k3-c2 blogsite __init__
source_atoms:
- atom-los-facts-de-python-traen-bases-decoradores-llamadas-y-asignaciones-genéricas-que-specir-interpreta
target_kind: test
target_identity: tests/fixtures/treesitter/blog_app/blogsite/__init__.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# k3-c2 blogsite __init__

## Intent

materializa en tests/fixtures/treesitter/blog_app/blogsite/__init__.py el atom atom-los-facts-de-python-traen-bases-decoradores-llamadas-y-asignaciones-genéricas-que-specir-interpreta
