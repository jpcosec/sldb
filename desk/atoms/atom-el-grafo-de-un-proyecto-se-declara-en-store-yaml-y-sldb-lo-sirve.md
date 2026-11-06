---
id: atom-el-grafo-de-un-proyecto-se-declara-en-store-yaml-y-sldb-lo-sirve
title: El grafo de un proyecto se declara en store.yaml y sldb lo sirve
five_wh_one_plus: what
tags:
- system:sldb
- topic:project-graph
provenance: docs/architecture/project-graph.md
---

# El grafo de un proyecto se declara en store.yaml y sldb lo sirve

## Answer

El grafo de proyecto (los nodos que son documentos, rutas trackeadas y superficies no modeladas, y las aristas que salen de sus campos de referencia y menciones) se declara como datos en la configuración project_graph de store.yaml, sin callables, y sldb lo construye, lo memoiza y lo sirve: sldb.api da nodos, aristas, edges_to (referencias entrantes) y faltantes; la CLI es sldb graph project nodes|edges|missing; sldb serve expone GET /project-graph/* y /edges?include_linked. Una superficie declara closed: para marcar qué documentos cuentan como cerrados (closed_document queda como argumento Python deprecated hasta que deskops lo deje en CC33). Un consumidor como deskops ya no reescanea el repo para su grafo: lo lee de sldb. Implementado en GD21 (plan generalizar-desde-deskops); produce G_PROJECT_GRAPH.
