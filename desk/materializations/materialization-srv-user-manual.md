---
sldb:
  by: agent
  at: '2026-11-17T15:28:40Z'
  authority: generated
  via: create_document
id: materialization-srv-user-manual
title: srv user-manual
source_atoms:
- atom-la-tabla-de-la-sección-10-del-manual-es-la-lista-de-rutas-http-de-sldb-serve-y-un-test-la-compara-co
target_kind: doc
target_identity: docs/user-manual.md
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_serve.py
tags:
- system:sldb
- topic:serve
---

# srv user-manual

## Intent

materializa en docs/user-manual.md el atom atom-la-tabla-de-la-sección-10-del-manual-es-la-lista-de-rutas-http-de-sldb-serve-y-un-test-la-compara-co
