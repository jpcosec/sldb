# Brief: generalizar en sldb lo que deskops reimplementa

Fecha: 2026-11-05. Repo dueño: sldb. Estado: plan autorizado por el dueño (2026-11-05, decisiones.md DA1-DA6 y G4), `execution_authorized: true`; GD23, GD24 y GD26 por promover (bloqueados: el desk de sldb necesita deskops desk update --apply para registrar TaskCodeDoc). Rama P2 del árbol aprobado por el dueño (`~/proyectos/SLDB_1/deskops-como-config-arbol.md`). Hermano de `grafo-operable` (P1, mismo desk) y productor de los habilitadores `T2.x` que consume el plan `deskops-como-config` de deskops (P3, P5).

## Encargo

Que la mecánica genérica que deskops reimplementa en Python (escanear el repo para armar un grafo, buscar y reescribir referencias entrantes, seleccionar documentos por glob/prefijo/campo, transacciones de varios documentos, vistas compuestas, scaffold de un store, jerarquía de tags y reemplazo de texto en documentos trackeados) viva en la API de sldb (`sldb.api`, CLI y `sldb serve`), declarada por datos y probada en sldb, de modo que deskops quede como configuración del caso más un CLI delgado.

## Por qué ahora

- El dueño decidió el 2026-11-05 (G1 en `decisiones.md`): lo general va a sldb y lo específico del caso deskops va a deskops; deskops es configuración sobre sldb.
- El Board de la UI tardaba ~100 s porque `deskops/graph/extract_*.py` reescanea el repo en vez de leer el índice de aristas de sldb. La rama en vuelo `wt/closeout-graph-sldb` (sldb `432e45d6`, deskops `7a2ec23b`/`9ced34e5`) ya movió el núcleo a `sldb.api.edges.project_graph` y bajó el Board a ~0.36 s caliente; falta cerrarlo como API declarada por datos y servida (GD21).
- deskops tiene ~18.7k líneas; `doc_io.DocTransaction`, `desk_view.py`, `workspace.py`, `domain_tree.py`, los escaneos `rglob` de `services/atoms.py`/`retire.py`/`drawer.py` y los selectores de `desk_paths.py` son mecánica de store, no de workflow (ver `alcance.md` §Estado de partida).
- Sin estas capacidades, el plan de deskops (P3) no puede borrar su código: cada superficie de deskops se cambia y su código viejo se borra en el mismo paso, y eso exige que sldb tenga el reemplazo.

## Resultado esperado del plan completo

1. **Grafo de proyecto** (GD21): nodos de documentos trackeados, superficies no modeladas y archivos fuente, aristas declaradas (índice) y menciones por patrón, todo desde una configuración de datos (`ProjectGraphConfig` serializable, declarable en `store.yaml`), servido por `sldb serve` y con aristas entrantes.
2. **Referencias entrantes** (GD22): `referrers(store, target)` (aristas de campo y menciones en prosa, con ubicación) y `rewrite_references(store, old, new | None)` que reescribe o quita el valor en cada documento y lista, dentro de una transacción.
3. **Selectores** (GD23): `select_documents(store, selector)` con formas id exacto, prefijo único, glob de ruta, `model <= X` y `where`, sobre la proyección del índice (sin re-extraer Markdown).
4. **Transacción** (GD24): `sldb.api.transaction(store)` anidable con rollback total (archivos, entradas, shards) y `apply_batch(store, changes)` con operaciones create/update/delete/move/track/untrack/write_file y guarda por `source_hash`; `/save` delega en ella.
5. **Vistas declaradas** (GD25): `ViewDoc` con secciones (selector, campos, aristas, agrupación, reglas), `sldb views run` y `GET /views/<nombre>` con revisión (ETag).
6. **Scaffold declarado** (GD26): `store.yaml` declara carpetas y semillas (`if_missing` | `managed`); `sldb stores scaffold [--apply]` con reporte; `build_store` pasa a `sldb.api`.
7. **Tags y reemplazo** (GD27): espacios de nombres de tags declarados y validados, guarda de padres documentados, árbol con huérfanos, y `replace_text` con conteo exacto sobre un documento trackeado.

## El límite (lo que este plan no promete)

- **No es el lenguaje de reglas.** Lenguaje, `RuleDoc`, anclas `doc:`, evaluación en escritura y transiciones como datos son de `grafo-operable` (GO04–GO10). Este plan los consume donde los nombra (`requires` con gates `G_GO*`) y no los adelanta ni los duplica.
- **No cambia deskops.** deskops borra su código en su propio plan (`deskops/desk/drawer/plans/deskops-como-config/`). La única escritura en otro repo es la nota por el canal entre desks (`deskops message send --to deskops`).
- **No modela el workflow de deskops.** Nada en sldb sabe de tareas, Board, rituales, pills ni closeout: los nombres del caso viven en la configuración de deskops. Un test de sldb que necesite un caso usa modelos de prueba propios.
- **No calcula hechos de git.** Commits, ramas y existencia de tests siguen siendo de quien los consume.

## Vocabulario

- **Configuración de grafo de proyecto**: datos que dicen qué superficies son documentos, qué archivos son nodos, qué campos son aristas y qué patrones de texto son menciones.
- **Mención**: arista extraída por patrón de texto (regex declarada) desde el cuerpo o una sección de un documento; no es campo de modelo.
- **Selector**: expresión que resuelve a una lista ordenada de documentos del store.
- **Transacción**: unidad de escritura de varios documentos y archivos con rollback total ante excepción.
- **Vista**: documento `ViewDoc` que compone selectores, campos, aristas y reglas en un payload con nombre y revisión.
- **Semilla**: archivo o documento que el scaffold escribe si falta (`if_missing`) o mantiene igual a la declaración (`managed`).

## Fuera de alcance

Cambios en deskops, graph_ui o en otros desks; motor de grafo externo; autenticación (`sldb serve --token` ya existe y no se toca); el lenguaje de reglas y su evaluación (grafo-operable); migración de stores ajenos (cada desk adopta al subir de versión).
