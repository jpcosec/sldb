---
id: atom-una-operación-de-sldb-se-ancla-al-store-más-cercano-no-al-directorio-desde-donde-se-corre
title: Una operación de sldb se ancla al store más cercano, no al directorio desde
  donde se corre
five_wh_one_plus: where
tags:
- system:sldb
- topic:federation
- topic:store-context
provenance: src/sldb/store/resolver.py
---

# Una operación de sldb se ancla al store más cercano, no al directorio desde donde se corre

## Answer

sldb resuelve el contexto desde el store más cercano que encierra el directorio actual (sin contar el global ~/.sldb), salvo un --store explícito: así FAQ, explore, alias y federación leen lo mismo desde la raíz que desde un subdirectorio. La federación recorre los stores enlazados en anchura y una vez cada uno (src/sldb/store/edge_index/federation.py:federated_stores), así que dos stores que se enlazan entre sí no hacen ciclo. El catálogo global se mantiene al hacer init y se reconcilia de forma explícita (sldb stores reconcile).
