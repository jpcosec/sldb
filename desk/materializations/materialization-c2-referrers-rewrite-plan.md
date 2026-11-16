---
sldb:
  by: agent
  at: '2026-11-16T15:06:37Z'
  authority: generated
  via: create_document
id: materialization-c2-referrers-rewrite-plan
title: c2-referrers rewrite_plan
source_atoms:
- atom-referrers-y-rewrite-references-trabajan-sobre-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-cuent
target_kind: code
target_identity: src/sldb/api/edges/rewrite_plan.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
tags:
- system:sldb
- topic:clean-code
---

# c2-referrers rewrite_plan

## Intent

materializa en src/sldb/api/edges/rewrite_plan.py el atom atom-referrers-y-rewrite-references-trabajan-sobre-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-cuent
