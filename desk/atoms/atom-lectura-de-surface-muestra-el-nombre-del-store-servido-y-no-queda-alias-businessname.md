---
sldb:
  by: agent
  at: '2026-11-25T18:06:49Z'
  authority: generated
  via: create_document
id: atom-lectura-de-surface-muestra-el-nombre-del-store-servido-y-no-queda-alias-businessname
title: Lectura de surface muestra el nombre del store servido y no queda alias businessName
five_wh_one_plus: how
tags:
- system:sldb
- topic:surface-lectura
---

# Lectura de surface muestra el nombre del store servido y no queda alias businessName

## Answer

surface pide GET /stores con SldbClient.storeInfo() y WorkbenchShell pasa la ruta servida a storeTitle; mientras carga o si falla muestra 'Documentos'. El alias businessName de wiki-index se borró sin sustituto.
