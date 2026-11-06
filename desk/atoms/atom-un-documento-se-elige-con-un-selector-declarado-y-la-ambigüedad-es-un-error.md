---
id: atom-un-documento-se-elige-con-un-selector-declarado-y-la-ambigüedad-es-un-error
title: Un documento se elige con un selector declarado y la ambigüedad es un error
five_wh_one_plus: what
tags:
- system:sldb
- topic:selectors
- topic:query-api
provenance: docs/architecture/selectors.md
---

# Un documento se elige con un selector declarado y la ambigüedad es un error

## Answer

sldb elige documentos con un selector declarado como datos, no con código del consumidor: un mapa con ref (export_id o Model:name, con alias de store enlazado), prefix, path_glob (semántica de pathlib: * no cruza /, ** sí), model (incluye subclases), where (gramática de rules-language) e include_linked, combinados por conjunción. sldb.api.select_documents(store, selector, expect) devuelve filas {export_id, model, name, path}; con expect='one', ninguno es SLDBDocumentTargetError y varios es AmbiguousSelectionError con los candidatos, nunca una elección silenciosa. La misma selección está en sldb docs select y en GET /docs/select (404 y 409). El núcleo vive en el store (store/query_engine) y la API es su cara pública. sldb find --where sigue evaluando sobre el payload de cada documento, no sobre la proyección del índice. Implementado en GD23 (plan generalizar-desde-deskops); reemplaza a deskops/desk_paths.py resolve_selector.
