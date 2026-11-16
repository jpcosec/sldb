---
sldb:
  by: agent
  at: '2026-11-16T11:19:09Z'
  authority: generated
  via: create_document
id: materialization-template-anchors-template-extractor
title: template-anchors template_extractor
source_atoms:
- atom-sldb-api-template-anchors-dice-por-campo-de-un-modelo-el-párrafo-literal-de-la-plantilla-que-ancla-s
target_kind: code
target_identity: src/sldb/core/template_extractor.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_literal_paragraph_anchor.py
tags:
- system:sldb
- topic:templates
---

# template-anchors template_extractor

## Intent

materializa en src/sldb/core/template_extractor.py el atom atom-sldb-api-template-anchors-dice-por-campo-de-un-modelo-el-párrafo-literal-de-la-plantilla-que-ancla-s
