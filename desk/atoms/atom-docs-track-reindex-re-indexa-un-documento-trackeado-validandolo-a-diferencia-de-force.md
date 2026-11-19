---
sldb:
  by: agent
  at: '2026-11-19T10:57:47Z'
  authority: generated
  via: create_document
id: atom-docs-track-reindex-re-indexa-un-documento-trackeado-validandolo-a-diferencia-de-force
title: docs track --reindex re-indexa un documento trackeado validándolo, a diferencia
  de --force
five_wh_one_plus: how
tags:
- system:sldb
- topic:cli
---

# docs track --reindex re-indexa un documento trackeado validándolo, a diferencia de --force

## Answer

sldb docs track <path> --reindex (y track_document_file(..., reindex=True)) re-indexa desde el archivo un documento ya trackeado en la misma ruta. Corre antes de escribir las mismas validaciones que un track normal (round-trip del modelo, ruido estructural, frontmatter no declarado). Si el archivo no valida, falla con ese error y no escribe nada, así que el índice queda igual. Sobre un documento no trackeado se comporta como track. --force sigue re-indexando sin esas validaciones, y --reindex con --force juntos los rechaza argparse.
