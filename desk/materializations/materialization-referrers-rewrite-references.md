---
sldb:
  by: agent
  at: '2026-11-16T11:32:27Z'
  authority: generated
  via: create_document
id: materialization-referrers-rewrite-references
title: referrers rewrite_references
source_atoms:
- atom-referrers-y-rewrite-references-trabajan-sobre-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-cuent
target_kind: code
target_identity: src/sldb/api/edges/rewrite_references.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_referrers.py
  tests/api/test_rewrite_references.py
tags:
- system:sldb
- topic:references
---

# referrers rewrite_references

## Intent

materializa en src/sldb/api/edges/rewrite_references.py el atom atom-referrers-y-rewrite-references-trabajan-sobre-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-cuent
