---
id: atom-un-mapa-de-hashes-vacio-significa-no-se-pudo-calcular-nunca-nada-cambio
title: Un mapa de hashes vacio significa 'no se pudo calcular', nunca 'nada cambio'
five_wh_one_plus: how_not
tags:
- system:sldb
- topic:hashing
- topic:merkle-tree
- topic:diagnostics
- topic:backward-compatibility
provenance: src/sldb/store/diagnostics.py
---

# Un mapa de hashes vacio significa 'no se pudo calcular', nunca 'nada cambio'

## Answer

Al agregar field_hashes junto a content_hash en el store de sldb, la tentacion es tratar un mapa vacio como 'ningun campo cambio'. Es incorrecto: un store escrito antes de que field_hashes existiera, o un documento que ya no extrae, tambien producen mapa vacio. Si el diagnostico dijera 'cero campos cambiaron' ahi, estaria contradiciendo a content_hash, que ya dijo que SI cambio algo. Por eso _changed_fields en store/diagnostics.py devuelve vacio cuando falta cualquiera de los dos lados de la comparacion, y el lector cae al documento entero. La regla general: ausencia de dato no es dato. 'No se pudo calcular' y 'se calculo y dio cero' son estados distintos y colapsarlos produce diagnosticos que se contradicen entre si. Aplica a cualquier capa derivada que se agregue al lado de un hash existente, incluido el embedding por campo que sigue a este trabajo.
