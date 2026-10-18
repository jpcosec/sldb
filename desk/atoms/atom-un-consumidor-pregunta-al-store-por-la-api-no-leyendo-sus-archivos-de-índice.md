---
id: atom-un-consumidor-pregunta-al-store-por-la-api-no-leyendo-sus-archivos-de-índice
title: Un consumidor pregunta al store por la API, no leyendo sus archivos de índice
five_wh_one_plus: how_not
tags:
- system:sldb
---

# Un consumidor pregunta al store por la API, no leyendo sus archivos de índice

## Answer

No parsear .sldb/core/store_index.yaml desde otro repo para saber qué modelos hay: su forma es interna y cambia (origin, family). sldb.api.registered_models e is_model_registered (nombre, module:Class o module.Class) y sldb models check son la superficie estable.
