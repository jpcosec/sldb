---
id: atom-el-template-de-un-modelo-es-estable-sus-recetas-se-calculan-una-vez-no-en-cada-extract
title: 'El template de un modelo es estable: sus recetas se calculan una vez, no en
  cada extract'
five_wh_one_plus: how
tags:
- system:sldb
- topic:performance
- topic:parsing
provenance: src/sldb/runtime/validation.py
---

# El template de un modelo es estable: sus recetas se calculan una vez, no en cada extract

## Answer

Las recetas de extracción de sldb dependen solo del string __template__ del modelo, no del documento: se memoizan por template (runtime/validation.py:_recipes, lru_cache). Rehacerlas en cada extract y validate era el mayor costo evitable del pipeline (~35% de la extracción en el store de sldb). Lo mismo vale para el parser markdown-it: uno por proceso, no uno por documento. Lo que sí depende del documento (su AST) se parsea una vez por texto.
