---
id: atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta
title: Una vista es un documento que declara qué leer y sldb la ejecuta
five_wh_one_plus: what
tags:
- system:sldb
- topic:views
provenance: docs/architecture/views.md
---

# Una vista es un documento que declara qué leer y sldb la ejecuta

## Answer

Una vista de sldb es un ViewDoc (el de SV01) con params y sections, sin código: cada sección declara select (un selector de GD23, con sustitución {param}), fields, edges (vecinos por relación y dirección), group_by y group_order, rules (RuleDocs de GO06 cuyos findings se agregan a cada fila) y transitions (aristas que se cumplen y bloqueadas, de GO08/GO09). sldb.api.run_view(store, name, params) devuelve las secciones con una revision (sha256 de lo leído) y sldb serve la expone en GET /views/<name> con ETag y 304. Un hecho que sldb no calcula entra como documento que la vista lee, nunca como proveedor computed en Python (DA1). El nombre projection queda reservado para las rutas de SV02. Implementado en GD25 (plan generalizar-desde-deskops).
