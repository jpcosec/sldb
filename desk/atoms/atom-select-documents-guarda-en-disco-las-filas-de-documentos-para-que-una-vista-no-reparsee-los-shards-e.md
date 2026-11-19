---
sldb:
  by: agent
  at: '2026-11-19T16:54:45Z'
  authority: generated
  via: create_document
id: atom-select-documents-guarda-en-disco-las-filas-de-documentos-para-que-una-vista-no-reparsee-los-shards-e
title: select_documents guarda en disco las filas de documentos para que una vista
  no reparsee los shards en cada proceso
five_wh_one_plus: how
tags:
- system:sldb
- topic:views
---

# select_documents guarda en disco las filas de documentos para que una vista no reparsee los shards en cada proceso

## Answer

select_documents (src/sldb/store/query_engine/document_rows_disk.py) guarda en .sldb_cache/document_rows/ un JSON con las filas de documentos que necesita. La clave sale de stats y hashes, sin leer los shards que se quieren evitar: índice del store, índice y roster hash de cada modelo, stat de los directorios de shards y versión del índice. Ante cualquier diferencia, o con una caché corrupta o de otra versión, lee los shards como antes. networkx se importa perezoso y store.yaml se carga con CSafeLoader. Con eso, sldb views run board en el layout de H11 bajó de 2,48 s a 1,43 s (mediana, caliente); la meta de 1 s no se alcanza y el informe del ejecutor explica el resto.
