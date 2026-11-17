---
sldb:
  by: agent
  at: '2026-11-16T23:58:02Z'
  authority: generated
  via: create_document
id: atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
title: Un conflicto de git en los índices derivados de .sldb se resuelve con el merge
  driver y sldb stores rebuild-index
five_wh_one_plus: what
tags:
- system:sldb
- topic:store
provenance: tarea j02 (decisión 2 de JP, integrada con H2 de velocidad-hooks), ejecutor
  deskops-e-d029d60e0080, tester deskops-t-1324db7bbee4 PASA
---

# Un conflicto de git en los índices derivados de .sldb se resuelve con el merge driver y sldb stores rebuild-index

## Answer

Una vez por clon: sldb stores merge-driver --install (idempotente) registra en .gitattributes y git config un driver para .sldb/store.yaml, .sldb/core/store_index.yaml y .sldb/core/models/*.yaml: une stores, modelos, links, predicados e include de los dos lados, sin marcadores. Después de cada merge o rebase que toque .sldb/: sldb stores rebuild-index regenera los índices derivados (también repara un archivo con marcadores o que no parsea). Sin driver, cargar un índice con marcadores o corrupto falla con un error que nombra el comando a correr. stores init alerta si otra rama local ya tiene un store: un store por repositorio. Procedimiento en AGENTS.md y docs/versionado-y-colaboracion.md.
