---
sldb:
  by: agent
  at: '2026-11-16T11:32:06Z'
  authority: generated
  via: create_document
id: materialization-referrers-referrers
title: referrers referrers
source_atoms:
- atom-referrers-y-rewrite-references-trabajan-sobre-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-cuent
target_kind: code
target_identity: src/sldb/api/edges/referrers.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_referrers.py
  tests/api/test_rewrite_references.py
tags:
- system:sldb
- topic:references
---

# referrers referrers

## Intent

materializa en src/sldb/api/edges/referrers.py el atom atom-referrers-y-rewrite-references-trabajan-sobre-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-cuent
