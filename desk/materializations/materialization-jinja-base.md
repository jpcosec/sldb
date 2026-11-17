---
sldb:
  by: agent
  at: '2026-11-17T13:19:48Z'
  authority: generated
  via: create_document
id: materialization-jinja-base
title: jinja base
source_atoms:
- atom-solo-la-plantilla-del-modelo-es-jinja-el-valor-de-un-campo-se-renderiza-literal
target_kind: code
target_identity: src/sldb/core/renderer_engine/base.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_list_items_round_trip.py
tags:
- system:sldb
- topic:render
---

# jinja base

## Intent

materializa en src/sldb/core/renderer_engine/base.py el atom atom-solo-la-plantilla-del-modelo-es-jinja-el-valor-de-un-campo-se-renderiza-literal
