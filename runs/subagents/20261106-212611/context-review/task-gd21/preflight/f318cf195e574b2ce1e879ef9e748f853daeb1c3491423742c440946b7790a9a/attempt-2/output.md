## REFORMULACION

Encargo ejecutable (task.code, no agregado): sobre la rama `wt/closeout-graph-sldb` ya integrada en main de sldb (fe36893f), convertir la configuración del grafo de proyecto en dato puro (from_mapping/to_mapping con ida y vuelta exacta, declarada en `store.yaml` bajo `project_graph`, validación propia, `closed:` como predicado del lenguaje en vez de callable), añadir `ProjectGraph.edges_to` con mapa inverso memoizado por firma de shards y mtime de superficies, y exponer `sldb.api.project_graph(store)`, CLI `sldb graph project nodes|edges|missing` con envelope, rutas `/project-graph/*` y `/edges?include_linked=`, más tests, CHANGELOG y `docs/architecture/project-graph.md`. Límites: solo los archivos listados; nada de extractores/oráculo deskops (CC33), ni nombres del caso deskops en `src/sldb/`, ni GD22; salidas existentes intactas (aditivo). Produce G_PROJECT_GRAPH y nota a deskops.

## AMBIGUEDADES

1. "el hook closed_document deja de ser callable" — no dice qué ocurre con configuraciones existentes que lo usen: ¿error, migración o ignorar? Obligaría a inventar política de compatibilidad.
2. "tocar un archivo incluido hace que la siguiente recalcule" y "mtime de las superficies no modeladas" — no define si cuentan archivos excluidos por `FileExclusions` ni qué es exactamente "incluido". Obligaría a inventar el conjunto de mtime observado.
3. "las tres rutas de /project-graph responden lo mismo que la CLI" — "lo mismo" no fija si es equivalencia de datos o de envelope JSON idéntico. Obligaría a inventar el contrato de respuesta HTTP.
4. "una configuración con un callable o con una clave desconocida falla al cargar con un mensaje que nombra la clave" — un callable no tiene clave; no se sabe qué debe nombrar el mensaje. Obligaría a inventar el formato de error.
5. Validación pide `pytest tests/test_store_seams.py`, ausente de `files:`; y "sin líneas nuevas en src/sldb/ contra origin/main" choca con añadir módulos nuevos. Obligaría a inventar alcance del grep y autorización de archivo.

## DRY-RUN

Lecturas: los 22 archivos listados, `store_declaration.py`, `where.py`, `edge_reading.py`, `shard_signature.py`, goldens de serve. Cambios: config dataclasses con to/from_mapping; validación en StoreDeclaration; `closed` evaluado con `where_matches`; mapa inverso + memo; `edges_to`; `api/__init__`; parsers/comandos; rutas nuevas y `include_linked`; tests; docs; CHANGELOG. Dependencias: GO04/GO05 cerrados, rama base presente, `sldb.api.where`. Validaciones futuras: los cuatro pytest, greps de genericidad, CLI sobre store temporal, `test_clean_code_rules`, rebase.

## FUTURO

Deciden fuera: supervisor (revisión en frío, suite completa, poda de `files:` no usados), deskops en CC33 (oráculo de equivalencia contra su configuración), quien opera el desk (correcciones del TaskDoc y `coordinator-status.md`), y la recepción de la nota de cierre.
