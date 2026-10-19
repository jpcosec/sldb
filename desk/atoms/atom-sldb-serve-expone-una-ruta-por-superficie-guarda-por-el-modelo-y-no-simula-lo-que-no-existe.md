---
id: atom-sldb-serve-expone-una-ruta-por-superficie-guarda-por-el-modelo-y-no-simula-lo-que-no-existe
title: sldb serve expone una ruta por superficie, guarda por el modelo y no simula
  lo que no existe
five_wh_one_plus: how_not
tags:
- system:sldb
- topic:serve
- topic:api
provenance: src/sldb/cli/serve/
---

# sldb serve expone una ruta por superficie, guarda por el modelo y no simula lo que no existe

## Answer

Las superficies de sldb (AST, campos, secciones, segmentos, modelos, grafo, aristas, stores) se consultan cada una por su propia ruta en src/sldb/cli/serve/*_routes.py, igual que por su comando (sldb ast, sldb fields...), y no por un endpoint monolítico que mezcle todo para una vista. Un endpoint único acopla a todos los consumidores a la forma de una pantalla y esconde qué superficie falló. Guardar un documento pasa por el modelo (save_single llama a save_payload, que vuelve a renderizar con el template), así que el frontmatter se conserva como datos del modelo y no se pierde ni se reescribe a mano. Una superficie que todavía no existe no se simula con un estado 'coming soon' o un mock: se responde lo que hay, y lo que falta se informa explícitamente, como hace unavailable_models.py con los modelos que no se pudieron importar. El principio llegó como átomo v1 a pron (merge 49c647a) y vuelve a sldb, que es donde se aplica.
