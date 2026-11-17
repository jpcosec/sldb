---
sldb:
  by: agent
  at: '2026-11-17T13:20:27Z'
  authority: generated
  via: create_document
id: materialization-jinja-test-list-items-round-trip
title: jinja test_list_items_round_trip
source_atoms:
- atom-solo-la-plantilla-del-modelo-es-jinja-el-valor-de-un-campo-se-renderiza-literal
target_kind: test
target_identity: tests/test_list_items_round_trip.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_list_items_round_trip.py
tags:
- system:sldb
- topic:render
---

# jinja test_list_items_round_trip

## Intent

materializa en tests/test_list_items_round_trip.py el atom atom-solo-la-plantilla-del-modelo-es-jinja-el-valor-de-un-campo-se-renderiza-literal
