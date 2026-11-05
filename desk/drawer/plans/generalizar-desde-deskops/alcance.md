# Alcance y estado de partida

## Estado de partida de sldb (verificado 2026-11-05, `main` + rama en vuelo)

- **Aristas.** `sldb.api.edges.edge_reading`: `load_edge_index` (:14), `edges_from(store, export_id, relation, include_linked, exclude_tags)` (:31), `edges_to` (:47), `edge_node` (:52), `edge_nodes_of_type` (:57); `edges_holding` (`edges_holding.py:13`); `unresolved_references` (`unresolved_references.py:12`). Composición memoizada por firma de shards en `store/edge_index/compose.py:22` (`_COMPOSED` :19, `shard_signature.py:22`). Las aristas de esquema llevan `metadata = {origin: schema, field, declared}` (`store/edge_index/declared_references.py:68`): alcanza para ubicar el campo que guarda la referencia.
- **Grafo de proyecto (rama `wt/closeout-graph-sldb`, sldb `432e45d6`, sin integrar).** `src/sldb/api/edges/project_graph/` (37 módulos): `ProjectGraph(root, ProjectGraphConfig)` con `node_ids()`, `edges_from(node_id)` perezoso, `missing_from`, `extraction()`; dataclasses de configuración `DocumentSurface`, `FileRule`, `FileExclusions`, `DeclaredFileTargets`, `ReferenceField`, `MentionPattern`, `SectionMentions`, `LineMentions`, `MissingTargetKind`; recorrido `os.walk` con poda (`project_file_walk.py:13`); `tracked_documents(store, refs)` (`api/stores/tracked_documents.py:20`). Pendiente: `closed_document` es un callable (la configuración no es dato puro), sin aristas entrantes, sin rutas de `sldb serve` (propuesta en deskops `runs/subagents/20261105-closeout-graph-sldb/sldb-serve-note.md`: `/project-graph/nodes|edges|missing`).
- **Selectores.** `where_matches(expr, payload, subject)` (`api/where.py:10`); `search(...)` (`api/search.py:26`, `/find`); `doc_status(store, ref)` (`api/stores/doc_status.py:18`, ref = nombre, `Model/name`, ruta trackeada o `alias:`; `doc_ref.py:43` solo coincidencia exacta); `indexed_documents` (`api/stores/indexed_documents.py:15`); `glob_structural`/`find_structural` (`store/query_engine/structural_queries.py:12,18`) solo desde la CLI `query`. No hay prefijo único, glob de ruta ni filtro modelo+where sin término de búsqueda.
- **Escritura.** `/save` por lotes (`cli/serve/save_routes.py:35`): prevalida (`prepare_batch` :46), aplica create→update→delete (`apply_batch` :74, tope 500), guarda por igualdad de payload completo (`save_plan.py:51,59` → 409), crea solo en `default_document_path` (:63), rechaza cambio de modelo (:53); ante falla devuelve 500 con `completed` **sin rollback**. No hay batch en `sldb.api` (vive en la capa HTTP). Primitiva de rollback por operación: `store/io/rollback.py:11 rollback_on_error(paths, forget_caches)`. No existen move, untrack en lote, escritura de archivo no modelado ni ruta elegida al crear.
- **Serve.** Tabla estática en `cli/serve/routes.py:47-110` (GET `/health /schema /graph /edges* /graph/* /document* /models* /lint /stores* /corpus/rank /similar /fields /sections /ast /find /extract /render`; POST `/models/* /docs* /extract/segments /save`). `/edges` siempre con `include_linked=True` (`edges_routes.py:39`). `StructuredQuery` (`store/graph/language/structured_query.py:12`) solo por CLI `graph query`. Sin consultas con nombre, sin revisión por vista.
- **Store declarado.** `StoreDeclaration` (`api/stores/store_declaration.py:20`): `links, models, predicates, include, generate, derived, policy`; `apply_declaration.py` idempotente (`apply_links` :24, `apply_models` :33, `apply_includes` :56). `build_store` vive en `cli/commands/stores_build.py:35`, no en la API. No hay carpetas ni semillas.
- **Tags.** Jerarquía por prefijo con punto ya existe (`store/semantic_tags.py:35 _prefix_edges`), DAG semántico (`store/semantic_dag_sync.py:12`, `api/semantic/dag_reads.py:13`, `dag_writes.py`), no reexportado en `sldb.api`. No hay registro de espacios de nombres, guarda de padre documentado, árbol con huérfanos ni reemplazo de texto en documentos trackeados.
- **grafo-operable**: GO01–GO03 cerrados en main (GO03 = `804f1ad4`; su gate `G_SEAM` sigue `pending` en ese dag.yaml hasta que su desk lo marque); GO04 promovido (`1c09a9c5`); GO05–GO10 sin promover.

## Lo que reemplaza en deskops (para contexto; se borra en el plan de deskops)

| Nodo | Código de deskops que deja sin motivo | Nodo de deskops que lo borra |
|---|---|---|
| GD21 | `graph/extract_docs.py`, `extract_edges.py`, `extract_sources.py` (ya movidos a oráculo en la rama), `graph/checks.py` (`find_atom_reference_violations` rglob :124), `graph/snapshot.py` (construcción propia), `graph/self_reflection.py` (rglob) | CC33, CC34 |
| GD22 | `services/atoms.py:743 _find_inbound_atom_references`, `:764 _rewrite_inbound_atom_references`, `:809 _retarget_atom_documents`; `services/retire.py:213 _inbound_references`, `:158 _board_pill_updates`, `:141 _drawer_bullets_removed`; `services/drawer.py:183 _tasks_recording`; `services/closure.py:572-584` | CC35 |
| GD23 | `desk_paths.py:24 resolve_selector`; `operations.py:1125-1182` (`_resolve_glob`, `_resolve_artifact_selector[_multi]`, `_tracked_task_paths` que lee `.sldb` crudo, `_registered_repositories`), `:1259 _resolve_ritual_selector`; `services/issues.py:96,354`; `services/drawer.py:49,220` | CC35 |
| GD24 | `doc_io.py` entero (`DocTransaction` :250, `_RootTransaction` :180-244) | CC35 |
| GD25 | `services/desk_view.py` (composición de board/task/drawer/inbox) | CC34 |
| GD26 | `workspace.py:166-251` (`scaffold_desk`, `_write_if_missing`), `cli/commands/desk.py:100 guess_model_for_path`, `bootstrap.py` caídas a subprocess | CC36 |
| GD27 | `domain_tree.py` (guarda de padres, árbol), `atom_tags.py` (registro de espacios de nombres), `services/replace.py` | CC35 |

## Enlace con grafo-operable

Cada nodo declara en `requires` los gates `G_GO*` de este plan, que se satisfacen cuando el nodo GO homónimo cerró en `main` de sldb (closeout commit). Resumen:

| Nodo | Requiere (bloquea) | Coordina (no bloquea) | Por qué |
|---|---|---|---|
| GD21 | — | GO04 | el predicado `closed` usa `where_matches`; con GO04 se evalúa sobre la facet sin re-extraer, sin cambiar la API de GD21 |
| GD22 | — | GO07 | si GO07 cerró, reescribir un valor de un campo `__doc_anchors__` quita el `@sha256` para que sldb lo repinee; si no, esos campos no existen todavía |
| GD23 | GO04 | GO05 | `where` sobre la proyección, cero `Validator.extract`; con GO05 el selector acepta caminos sin cambiar su forma |
| GD24 | — | GO07, GO08 | comparten `payload_save_steps.py`; GD24 no lo edita y envuelve sus pasos; si GO08 cerró, se prueba el rollback ante una regla `on_write` error |
| GD25 | GO05, GO06, GO08 | GO09 | caminos en selectores, findings de reglas por fila, `edges_holding`/`edges_blocked` por fila (con `effects` de GO09) |
| GD26 | — | — | |
| GD27 | — | — | |

Lo que no está cerrado al promover un nodo se trata con la regla 6.

## Reglas comunes de ejecución

1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de sldb, con `--task-type` y `files` completos; antes, preflight TaskDoc-only y cold-bundle (ritual-context-review). Las revisiones en frío las decide el supervisor; quien opera el desk dispone los hallazgos como correcciones del TaskDoc (`deskops edit task`) y resume en `coordinator-status.md`; nada a mano en `desk/` fuera de `drawer/plans` ni en `.sldb/`.
2. Se ejecuta en robocop2, en un worktree de sldb aparte del de grafo-operable (otras áreas: edges, documents, serve, stores). Validación: los tests de los archivos tocados (`pytest -q <archivos>`, uno a la vez); la suite completa la corre el supervisor sobre el resultado integrado. Un nodo no cierra con tests rojos ni saltados.
3. Toda capacidad nueva entra con: función pública en `sldb.api` (reexportada en `sldb/api/__init__.py`), comando CLI con envelope JSON, ruta de `sldb serve` cuando el consumidor la necesita, pruebas, entrada en `CHANGELOG.md` y doc en `docs/architecture/`. Nada queda solo en el código.
4. Genericidad: ningún nombre del caso deskops (TaskDoc, Board, ritual, pill, atom, closeout) aparece en `src/sldb/` ni en sus tests, salvo como dato en fixtures. Un grep lo comprueba en la aceptación de cada nodo.
5. Compatibilidad: ninguna salida existente de la CLI ni de `sldb serve` cambia (goldens existentes verdes); lo nuevo es aditivo. Si un nodo necesita cambiar un contrato existente (p. ej. `/save` pasa a ser atómico), lo nombra en su aceptación y en el CHANGELOG.
6. Ante un contrato ausente de un nodo GO no cerrado, el nodo registra la hipótesis en su TaskDoc, implementa la parte que no depende de él y no inventa la API de grafo-operable.
7. Cada nodo, al cerrar, manda nota a deskops (`deskops message send --to deskops --kind suggestion`) con la función, el comando y la ruta nuevos y el código de deskops que quedan sin motivo (tabla de arriba); así se satisface el gate `G_GDxx` del plan de deskops.
8. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.
