---
id: atom-una-operación-que-crea-un-directorio-deshace-lo-que-alcanzó-a-crear-si-falla
title: Una operación que crea un directorio deshace lo que alcanzó a crear si falla
five_wh_one_plus: how
tags:
- system:sldb
---

# Una operación que crea un directorio deshace lo que alcanzó a crear si falla

## Answer

Si crear algo en disco falla a medias (permisos, disco, I/O), lo que alcanzó a escribirse se borra, pero solo si no existía antes, y el error dice dónde y qué revisar. Un resto parcial (un .sldb/ sin índice) es peor que nada: la próxima operación lo toma por un store roto. El código de salida distingue la precondición (2) de la falla a medias (1); ver src/sldb/api/stores/init_store.py:_write_or_undo.
