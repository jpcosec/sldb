---
sldb:
  by: agent
  at: '2026-11-20T10:12:43Z'
  authority: generated
  via: create_document
id: atom-los-comandos-cli-de-stores-instalan-solos-el-merge-driver-de-sldb-y-stores-check-avisa-si-falta
title: Los comandos CLI de stores instalan solos el merge driver de sldb, y stores
  check avisa si falta
five_wh_one_plus: how
tags:
- system:sldb
- topic:stores
---

# Los comandos CLI de stores instalan solos el merge driver de sldb, y stores check avisa si falta

## Answer

sldb stores init, sldb stores scaffold y sldb stores build (comandos de src/sldb/cli/commands/) llaman a ensure_merge_driver cuando el store está en un repo git: idempotente, nada fuera de git, aviso por stderr si git falla. Las funciones de API no lo instalan, para que un build dentro de una Transaction no deje cambios fuera del rollback. sldb stores check da el alert stores/merge_driver_missing con el fix 'sldb stores merge-driver --install'.
