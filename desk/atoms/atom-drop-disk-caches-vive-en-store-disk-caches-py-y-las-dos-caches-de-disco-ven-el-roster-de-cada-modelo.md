---
sldb:
  by: agent
  at: '2026-11-20T03:36:59Z'
  authority: generated
  via: create_document
id: atom-drop-disk-caches-vive-en-store-disk-caches-py-y-las-dos-caches-de-disco-ven-el-roster-de-cada-modelo
title: drop_disk_caches vive en store/disk_caches.py y las dos cachés de disco ven
  el roster de cada modelo
five_wh_one_plus: how
tags:
- system:sldb
- topic:cache
---

# drop_disk_caches vive en store/disk_caches.py y las dos cachés de disco ven el roster de cada modelo

## Answer

drop_disk_caches pasó de store/layout.py a src/sldb/store/disk_caches.py (layout.py vuelve a 80 líneas o menos), y stores build lo llama. La caché de filas de documentos y la compuesta incluyen el roster_hash de cada modelo en su clave, así que una reescritura in place dentro del mismo tick se ve en el siguiente proceso. El test de reescritura llama al sldb bajo prueba y no al instalado.
