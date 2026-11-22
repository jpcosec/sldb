---
sldb:
  by: agent
  at: '2026-11-22T13:55:34Z'
  authority: generated
  via: create_document
id: atom-el-guard-de-sobrescritura-con-perdida-acepta-quitar-un-encabezado-no-declarado-si-su-contenido-queda
title: El guard de sobrescritura con pérdida acepta quitar un encabezado no declarado
  si su contenido queda en el texto nuevo
five_wh_one_plus: how
tags:
- system:sldb
- topic:api
---

# El guard de sobrescritura con pérdida acepta quitar un encabezado no declarado si su contenido queda en el texto nuevo

## Answer

refuse_lossy_overwrite deja pasar una escritura de campo que quita un encabezado no declarado cuando su contenido (cuerpo calculado desde el mismo AST que scan_headings, setext e indentados incluidos), normalizado, está en el texto renderizado nuevo; si no puede calcular el cuerpo, rechaza (falla cerrado). Commits 291910691e0904df644b876c836f1104f749bb13 y 074bc3bc9754d1b2407ebcd4e27abee477964b34 (este último recuperado por el coordinador tras perderlo el reap). Agotó los dos intentos de tester; verificación del coordinador en runs/subagents/20261122-verif-guard-lossy/.
