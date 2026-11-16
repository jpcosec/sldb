---
sldb:
  by: agent
  at: '2026-11-16T11:19:29Z'
  authority: generated
  via: create_document
id: materialization-template-anchors-test-literal-paragraph-anchor
title: template-anchors test_literal_paragraph_anchor
source_atoms:
- atom-sldb-api-template-anchors-dice-por-campo-de-un-modelo-el-párrafo-literal-de-la-plantilla-que-ancla-s
target_kind: test
target_identity: tests/test_literal_paragraph_anchor.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_literal_paragraph_anchor.py
tags:
- system:sldb
- topic:templates
---

# template-anchors test_literal_paragraph_anchor

## Intent

materializa en tests/test_literal_paragraph_anchor.py el atom atom-sldb-api-template-anchors-dice-por-campo-de-un-modelo-el-párrafo-literal-de-la-plantilla-que-ancla-s
