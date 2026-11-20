---
sldb:
  by: agent
  at: '2026-11-20T02:53:49Z'
  authority: generated
  via: create_document
id: atom-las-caches-de-disco-de-sldb-ven-una-reescritura-in-place-de-un-documento-y-stores-build-las-invalida
title: Las cachés de disco de sldb ven una reescritura in place de un documento y
  stores build las invalida
five_wh_one_plus: how
tags:
- system:sldb
- topic:cache
---

# Las cachés de disco de sldb ven una reescritura in place de un documento y stores build las invalida

## Answer

La caché compuesta del índice de aristas (src/sldb/store/edge_index/composed_disk.py) incluye en su clave el roster_hash de cada modelo de cada store (roster_state en cache_keys.py), así que reescribir un documento in place, como hace deskops review dispose, la invalida aunque el reloj no avance. sldb stores build borra las cachés de disco composed/ y document_rows/ (drop_disk_caches en store/layout.py). Antes, una caché vieja dejaba a deskops sin ver recibos ya aceptados.
