---
sldb:
  by: agent
  at: '2026-11-16T11:33:09Z'
  authority: generated
  via: create_document
id: materialization-referrers-test-rewrite-references
title: referrers test_rewrite_references
source_atoms:
- atom-referrers-y-rewrite-references-trabajan-sobre-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-cuent
target_kind: test
target_identity: tests/api/test_rewrite_references.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_referrers.py
  tests/api/test_rewrite_references.py
tags:
- system:sldb
- topic:references
---

# referrers test_rewrite_references

## Intent

materializa en tests/api/test_rewrite_references.py el atom atom-referrers-y-rewrite-references-trabajan-sobre-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-cuent
