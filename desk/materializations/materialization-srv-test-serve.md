---
sldb:
  by: agent
  at: '2026-11-17T15:29:15Z'
  authority: generated
  via: create_document
id: materialization-srv-test-serve
title: srv test_serve
source_atoms:
- atom-la-tabla-de-la-sección-10-del-manual-es-la-lista-de-rutas-http-de-sldb-serve-y-un-test-la-compara-co
target_kind: test
target_identity: tests/test_serve.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_serve.py
tags:
- system:sldb
- topic:serve
---

# srv test_serve

## Intent

materializa en tests/test_serve.py el atom atom-la-tabla-de-la-sección-10-del-manual-es-la-lista-de-rutas-http-de-sldb-serve-y-un-test-la-compara-co
