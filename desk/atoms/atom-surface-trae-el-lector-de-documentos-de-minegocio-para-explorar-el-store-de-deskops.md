---
sldb:
  by: agent
  at: '2026-11-23T18:31:12Z'
  authority: generated
  via: create_document
id: atom-surface-trae-el-lector-de-documentos-de-minegocio-para-explorar-el-store-de-deskops
title: surface trae el lector de documentos de minegocio para explorar el store de
  deskops
five_wh_one_plus: how
tags:
- system:sldb
- topic:surface
---

# surface trae el lector de documentos de minegocio para explorar el store de deskops

## Answer

surface gana core/{doc-ref,wiki-index,rechazo,imagenes}.ts y workbench/{WikiIndex,Ficha,NuevaPagina,AvisoGuardado}.tsx con sus tests: indice por carpeta y semantica, lectura, ficha, referencias entre documentos y rechazos legibles; probado contra sldb serve sobre el store de deskops (/graph 4.6 s con 2085 docs, /document 68 ms, /document/segments 23 ms). WorkbenchShell.tsx, vite.config.ts y tsconfig sin cambios.
