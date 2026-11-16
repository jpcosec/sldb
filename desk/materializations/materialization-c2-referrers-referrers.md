---
sldb:
  by: agent
  at: '2026-11-16T15:04:54Z'
  authority: generated
  via: create_document
id: materialization-c2-referrers-referrers
title: c2-referrers referrers
source_atoms:
- atom-referrers-y-rewrite-references-trabajan-sobre-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-cuent
target_kind: code
target_identity: src/sldb/api/edges/referrers.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
tags:
- system:sldb
- topic:clean-code
---

# c2-referrers referrers

## Intent

materializa en src/sldb/api/edges/referrers.py el atom atom-referrers-y-rewrite-references-trabajan-sobre-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-cuent
