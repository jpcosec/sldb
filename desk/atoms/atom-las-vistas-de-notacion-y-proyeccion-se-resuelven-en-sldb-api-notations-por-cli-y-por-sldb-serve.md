---
id: atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve
title: Las vistas de notacion y proyeccion se resuelven en sldb.api.notations, por
  CLI y por sldb serve
five_wh_one_plus: where
tags:
- system:sldb
- topic:notations
- topic:serve
provenance: docs/architecture/notations-and-views.md
---

# Las vistas de notacion y proyeccion se resuelven en sldb.api.notations, por CLI y por sldb serve

## Answer

resolve_view, resolve_documents y evaluate_projection_view viven en sldb.api.notations y leen directamente del store; se exponen como sldb notations (list, sync, view, resolve) y en sldb serve bajo GET /notations, GET /notations/view, POST /notations/resolve y GET|POST /views/projection*. /views/<nombre> queda libre para las vistas compuestas de GD25. Ningun consumidor necesita YAML intermedio ni spec2viz para proyectar el grafo con una notacion. Decidido en SV02 (plan absorber-spec2viz-y-modelos-ui), integrado en ddc049b4 y 6ba8bb20.
