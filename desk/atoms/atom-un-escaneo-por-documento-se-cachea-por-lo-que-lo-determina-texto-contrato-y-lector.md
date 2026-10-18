---
id: atom-un-escaneo-por-documento-se-cachea-por-lo-que-lo-determina-texto-contrato-y-lector
title: 'Un escaneo por documento se cachea por lo que lo determina: texto, contrato
  y lector'
five_wh_one_plus: how
tags:
- system:sldb
- topic:performance
provenance: src/sldb/api/stores/scan_cache.py
---

# Un escaneo por documento se cachea por lo que lo determina: texto, contrato y lector

## Answer

Lo que stores check deriva de cada documento (si una reescritura perdería contenido, si trae headings no declarados) depende solo de su texto, del contrato de su modelo y del código de sldb que lo lee. Con esos tres como clave, en el caché del usuario y nunca dentro del store, un store sin cambios no se re-renderiza (src/sldb/api/stores/scan_cache.py). La huella del lector incluye el código, no solo la versión: en un checkout de desarrollo la versión no cambia cuando se arregla el extractor.
