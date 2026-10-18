---
id: atom-el-path-guardado-de-un-modelo-es-una-pista-model-ref-es-la-identidad
title: El path guardado de un modelo es una pista; model_ref es la identidad
five_wh_one_plus: how
tags:
- system:sldb
---

# El path guardado de un modelo es una pista; model_ref es la identidad

## Answer

En .sldb/core/store_index.yaml, el path de un modelo es relativo al proyecto o absoluto de la máquina donde se registró, y vacío para un modelo heredado: no es portable. model_ref (module:Class) sí lo es. Para encontrar la fuente se usa el path solo si es un archivo aquí, si no se importa model_ref (src/sldb/api/model_drafts/source_location.py).
