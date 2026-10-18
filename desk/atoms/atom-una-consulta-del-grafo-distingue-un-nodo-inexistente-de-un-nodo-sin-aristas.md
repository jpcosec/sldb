---
id: atom-una-consulta-del-grafo-distingue-un-nodo-inexistente-de-un-nodo-sin-aristas
title: Una consulta del grafo distingue un nodo inexistente de un nodo sin aristas
five_wh_one_plus: how
tags:
- system:sldb
---

# Una consulta del grafo distingue un nodo inexistente de un nodo sin aristas

## Answer

edges show (y cualquier lectura de aristas por nodo) devuelve [] tanto para un nodo real aislado como para un id que no existe. La CLI comprueba que el argumento sea un nodo del índice antes de imprimir [] y, si no lo es, falla y busca documentos cuyo export id termine en ':<argumento>' para sugerirlos: un documento se nombra Model:name, cualquier otro nodo sldb://<kind>/...
