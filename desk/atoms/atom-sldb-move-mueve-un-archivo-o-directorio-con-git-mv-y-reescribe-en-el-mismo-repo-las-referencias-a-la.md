---
sldb:
  by: agent
  at: '2026-11-20T04:28:26Z'
  authority: generated
  via: create_document
id: atom-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-reescribe-en-el-mismo-repo-las-referencias-a-la
title: sldb move mueve un archivo o directorio con git mv y reescribe en el mismo
  repo las referencias a la ruta vieja
five_wh_one_plus: how
tags:
- system:sldb
- topic:cli
---

# sldb move mueve un archivo o directorio con git mv y reescribe en el mismo repo las referencias a la ruta vieja

## Answer

sldb move <origen> <destino> [--dry-run] [--format json] mueve dentro del proyecto con git mv (o en disco si no está versionado); los documentos trackeados siguen trackeados con su nombre. En el mismo repo, todo string del payload de un documento que es la ruta vieja (o empieza por ella si el origen es un directorio) pasa a la nueva vía save_document_payload, y los links Markdown (inline, imágenes y referencias, resueltos desde el archivo que los contiene) apuntan a la nueva. Todo va en una Transaction; el índice de git se toca al final. --dry-run lista movimientos, campos y links sin tocar nada.
