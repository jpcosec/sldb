## REFORMULACION

**Propósito:** convertir la configuración del grafo de proyecto en dato puro declarado en `store.yaml`, sustituir el hook `closed_document` por el predicado `closed:`, añadir aristas entrantes `ProjectGraph.edges_to` memoizadas, y exponer API, CLI y rutas de `sldb serve`, con doc y CHANGELOG.
**Resultado:** `G_PROJECT_GRAPH` (artefacto no definido en el input): `ProjectGraphConfig` con ida y vuelta YAML, `closed:` evaluado con `where_matches`, `edges_to`, `sldb.api.project_graph(store)`, `sldb graph project nodes|edges|missing`, `GET /project-graph/*`, `/edges?include_linked=false`, `docs/architecture/project-graph.md`.
**Repo:** sldb, worktree aparte del de grafo-operable, sobre `wt/closeout-graph-sldb` ya integrada en main; promotor `deskops add task --from-drawer`.
**Límites:** fuera extractores y oráculo de deskops (CC33), nombres del caso deskops en `src/sldb/`, GD22; aditivo y compatible (regla 5); nada a mano en `desk/` ni `.sldb/` (regla 1).

## AMBIGUEDADES

1. «Produce G_PROJECT_GRAPH» — el input no define qué es ese artefacto ni cómo se comprueba; obligaría a inventar su forma (¿sección en el reporte, gate, fixture?).
2. «las pills ligadas, los átomos ligados» frente a `pills: []` y `atoms: []` del TaskDoc — no hay ninguno en el bundle; obligaría a inventar sus contenidos o a declarar que no existen.
3. «una segunda consulta sin cambios hace cero llamadas a os.walk/rglob» y «el grafo de proyecto se recalcula solo si cambia la firma» — no se dice si el memo vive por instancia, por proceso o en disco, ni si «segunda consulta» es otra llamada a `sldb.api.project_graph(store)` o el mismo objeto; obligaría a inventar la vida y ubicación de la caché.
4. «una configuración con un callable [...] falla al cargar con un mensaje que nombra la clave» — un YAML no porta callables; no se aclara si «cargar» es `from_mapping` en Python o `store.yaml`; obligaría a elegir la ruta y el mensaje.
5. «edges --from ID | --to ID» — la barra no aclara si son excluyentes, ambos obligatorios ni qué pasa sin ninguno; obligaría a inventar la validación de argumentos.
6. «el hook closed_document pasa a ser un predicado closed:» frente a q5, que «conserva SOLO como argumento Python [...] deprecated» — tensión sobre si el hook sobrevive; q5 es posterior, pero el Goal dice «pasa a ser».

## DRY-RUN

Lecturas: los `files:` del TaskDoc (config, `project_graph.py`, `project_texts.py`, store, `api/__init__.py`, parsers/commands, `routes.py`, `edges_routes.py`, tests, CHANGELOG), `where.py`, `shard_signature.py`, `edge_reading.py`.
Cambios previstos: `from_mapping/to_mapping` y campo `closed`; retirada/aviso de `closed_document`; rama `project_graph` en `StoreDeclaration`; `edges_to` con mapa inverso y memo por firma+stat; reexportes en `sldb.api`; subparsers y handlers `graph project`; `project_graph_routes.py` y despacho en `routes.py`; `include_linked` en `edges_routes.py`; tests y doc.
Dependencias: `where_matches`, `shard_signature`, `edges_from/edges_to`, `query_params`, envelope CLI.
Validaciones futuras: los `pytest` listados (uno a uno), `test_store_seams.py` sin editar, grep de regla 4 sobre el diff, salidas CLI del store temporal, nota a deskops, rebase sobre `origin/main`.

## FUTURO

CC33 corre el oráculo de equivalencia contra la configuración de deskops; el supervisor ejecuta la suite completa sobre lo integrado; el coordinador decide revisiones en frío y poda `files:` no usados; deskops migra `closed_document` y se borra; GD22 cubre aristas entrantes de escritura.
