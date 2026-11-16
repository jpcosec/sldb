---
sldb:
  by: agent
  at: '2026-11-16T11:18:27Z'
  authority: generated
  via: create_document
id: materialization-template-anchors-template-anchors
title: template-anchors template_anchors
source_atoms:
- atom-sldb-api-template-anchors-dice-por-campo-de-un-modelo-el-párrafo-literal-de-la-plantilla-que-ancla-s
target_kind: code
target_identity: src/sldb/api/model_registry/template_anchors.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_literal_paragraph_anchor.py
tags:
- system:sldb
- topic:templates
---

# template-anchors template_anchors

## Intent

materializa en src/sldb/api/model_registry/template_anchors.py el atom atom-sldb-api-template-anchors-dice-por-campo-de-un-modelo-el-párrafo-literal-de-la-plantilla-que-ancla-s
