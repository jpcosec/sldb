---
sldb:
  by: agent
  at: '2026-11-16T11:18:48Z'
  authority: generated
  via: create_document
id: materialization-template-anchors-init
title: template-anchors __init__
source_atoms:
- atom-sldb-api-template-anchors-dice-por-campo-de-un-modelo-el-párrafo-literal-de-la-plantilla-que-ancla-s
target_kind: code
target_identity: src/sldb/api/__init__.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_literal_paragraph_anchor.py
tags:
- system:sldb
- topic:templates
---

# template-anchors __init__

## Intent

materializa en src/sldb/api/__init__.py el atom atom-sldb-api-template-anchors-dice-por-campo-de-un-modelo-el-párrafo-literal-de-la-plantilla-que-ancla-s
