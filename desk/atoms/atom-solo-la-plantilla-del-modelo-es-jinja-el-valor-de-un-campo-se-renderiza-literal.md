---
sldb:
  by: agent
  at: '2026-11-17T13:19:01Z'
  authority: generated
  via: create_document
id: atom-solo-la-plantilla-del-modelo-es-jinja-el-valor-de-un-campo-se-renderiza-literal
title: Solo la plantilla del modelo es Jinja; el valor de un campo se renderiza literal
five_wh_one_plus: what
tags:
- system:sldb
- topic:render
provenance: tarea del render literal (nota de deskops 015212); ejecutor deskops-e-08683ea7876c,
  tester PASA en runs/subagents/20261116-test-jinja
---

# Solo la plantilla del modelo es Jinja; el valor de un campo se renderiza literal

## Answer

BaseRenderer.replace_markers reemplaza cada marcador por una referencia a una variable de contexto con nombre propio (una lista de valores indexada por marcador) y pasa los valores a Jinja como datos, así que el valor de un campo nunca se compila como plantilla: llaves, expresiones, comentarios y bloques de Jinja se guardan y vuelven byte a byte. El marcador opcional (optrev) y el render de los documentos existentes no cambian.
