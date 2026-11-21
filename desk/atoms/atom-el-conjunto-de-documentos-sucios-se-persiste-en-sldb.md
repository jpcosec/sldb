---
sldb:
  by: agent
  at: '2026-11-21T12:13:11Z'
  authority: generated
  via: create_document
id: atom-el-conjunto-de-documentos-sucios-se-persiste-en-sldb
title: El conjunto de documentos sucios se persiste en sldb
five_wh_one_plus: how
tags:
- system:sldb
- topic:store
---

# El conjunto de documentos sucios se persiste en sldb

## Answer

sldb persiste el conjunto de documentos sucios del store en vez de recalcularlo en cada proceso (commit del ejecutor con trailer Task-Id). El tester dio FALLA solo por la puerta 'identidad' por workbench_demo, la excepción autorizada (f055723d); los tests de la tarea y las regresiones relacionadas pasan.
