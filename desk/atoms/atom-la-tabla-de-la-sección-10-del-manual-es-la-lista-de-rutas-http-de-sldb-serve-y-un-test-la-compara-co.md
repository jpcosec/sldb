---
sldb:
  by: agent
  at: '2026-11-17T15:28:08Z'
  authority: generated
  via: create_document
id: atom-la-tabla-de-la-sección-10-del-manual-es-la-lista-de-rutas-http-de-sldb-serve-y-un-test-la-compara-co
title: La tabla de la sección 10 del manual es la lista de rutas HTTP de sldb serve
  y un test la compara con el código
five_wh_one_plus: what
tags:
- system:sldb
- topic:serve
provenance: tarea de rutas de serve (análisis del supervisor); ejecutor deskops-e-aa0321c9f2c0,
  tester PASA en runs/subagents/20261116-test-srv
---

# La tabla de la sección 10 del manual es la lista de rutas HTTP de sldb serve y un test la compara con el código

## Answer

docs/user-manual.md §10 tiene una fila por ruta de sldb serve (`MÉTODO /path` | parámetros | qué devuelve). test_user_manual_lists_every_serve_route en tests/test_serve.py arma la lista del código con los dicts de rutas importables de src/sldb/cli/serve/ más las comparaciones de route en routes.py leídas con ast, y falla en las dos direcciones si el manual y el código difieren. Una ruta nueva se documenta agregando su fila.
