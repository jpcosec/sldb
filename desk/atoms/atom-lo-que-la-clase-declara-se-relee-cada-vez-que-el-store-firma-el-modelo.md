---
id: atom-lo-que-la-clase-declara-se-relee-cada-vez-que-el-store-firma-el-modelo
title: Lo que la clase declara se relee cada vez que el store firma el modelo
five_wh_one_plus: how
tags:
- system:sldb
---

# Lo que la clase declara se relee cada vez que el store firma el modelo

## Answer

Todo lo que el store copia de la clase de un modelo (contrato, familia) se relee en stamp_model_node (src/sldb/store/model_node.py), por donde pasan todas las escrituras con la clase importada: lo que se copiaba una sola vez en models add (como __family__) quedaba congelado sin que nada lo señalara. Cuando la clase no importa se conserva lo registrado.
