---
sldb:
  by: agent
  at: '2026-11-17T08:34:42Z'
  authority: generated
  via: create_document
id: materialization-k3-c2-blogsite-urls
title: k3-c2 blogsite urls
source_atoms:
- atom-los-facts-de-python-traen-bases-decoradores-llamadas-y-asignaciones-genéricas-que-specir-interpreta
target_kind: test
target_identity: tests/fixtures/treesitter/blog_app/blogsite/urls.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
tags:
- system:sldb
- topic:code
---

# k3-c2 blogsite urls

## Intent

materializa en tests/fixtures/treesitter/blog_app/blogsite/urls.py el atom atom-los-facts-de-python-traen-bases-decoradores-llamadas-y-asignaciones-genéricas-que-specir-interpreta
