---
sldb:
  by: agent
  at: '2026-11-19T12:10:15Z'
  authority: generated
  via: create_document
id: atom-un-directorio-existente-declarado-como-target-de-una-materializacion-es-un-nodo-del-grafo-con-o-sin
title: Un directorio existente declarado como target de una materialización es un
  nodo del grafo, con o sin barra final
five_wh_one_plus: how
tags:
- system:sldb
- topic:graph
---

# Un directorio existente declarado como target de una materialización es un nodo del grafo, con o sin barra final

## Answer

declared_target_nodes crea un FileNode con file_kind directory para un target declarado que es un directorio existente dentro de la raíz del proyecto (sin expandirlo en nodos por archivo), y NodeLookup resuelve el target con o sin barra final (dir y dir/). Así graph missing de sldb y deskops graph missing dejan de reportarlo. Un directorio inexistente o fuera de la raíz sigue siendo missing.
