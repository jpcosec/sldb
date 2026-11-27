# Taxonomía de comandos

Fecha: 2026-11-27. Estado: **propuesta para que JP la apruebe**. Es el paso 1 del ADR
[One Command Taxonomy, Served By FastMCP](one-command-taxonomy-served-by-fastmcp.md). Es un
inventario y no cambia comportamiento. Quitar de la CLI lo marcado es otra tarea, la de la CLI
alineada con esta tabla.

## Cómo se lee

Cada operación de sldb aparece una vez, con el nombre que tiene hoy en cada una de las cuatro
caras: `sldb.api`, la CLI, `sldb serve` y `sldb mcp`. Un nombre que no es una operación (alias,
ayuda, ayudante interno, tipo de dato) está en la lista final "Sin operación", con su motivo.
`tests/test_command_taxonomy.py` compara este documento con el código: falla si una cara tiene
un nombre que no está aquí, o si aquí hay un nombre que la cara ya no tiene.

Criterio (JP, 2026-11-27): la tabla ordena, no conserva. Que alguien use un comando no es
razón para dejarlo; si otra operación hace lo mismo, se marca para reemplazo. Una operación
queda si es un sustantivo y un verbo propios, no por existir hoy en una cara.

Las operaciones siguen los ejes de JP del registro
[`ejes-y-anillos-de-operaciones`](../../desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md):
cada tipo de nodo y de arista admite crear, leer, cambiar y borrar; hay operaciones sobre el
store entero; y la navegación es una sola (partir de una dirección, seguir aristas, filtrar con
el lenguaje de predicados). El anillo es el de
[`docs/spec/mecanismos/anillos.md`](../spec/mecanismos/anillos.md); `caras` agrupa lo que solo
levanta una cara.

Columnas:

- **Operación**: nombre canónico propuesto, `sustantivo_verbo` en snake_case.
- **Efecto**: `lee`; `escribe` (escribe el store; una operación que lee y escribe es
  `escribe`); `externo` (git, archivos fuera del store, red, procesos).
- **Caras**: los nombres de hoy; `—` es que esa cara no la tiene. Las rutas de `serve` van con
  su método.
- **Marcas**: `dup`, más de un nombre para lo mismo en una cara; `renombre`, las caras usan
  palabras distintas para lo mismo; `hueco: <cara>`, falta en la CLI o en la API (que `serve` y
  `mcp` cubran menos es esperado: `serve` se retira y `mcp` escribe por `changes_apply`);
  `reemplazo → X`, propuesta de que salga y la cubra X; `retirar`, que salga sin reemplazo.

Qué se reutiliza: los `SurfaceDoc` de `knowledge/surfaces/`, que `sldb selfdoc sync` genera
desde el parser, ya listan los comandos de la CLI por grupo. Son una sola cara y por grupo, no
por operación, así que esta tabla los cita como fuente de la columna CLI y no los modifica.
Si JP aprueba la tabla, lo que sigue es que sea datos del store, revisados por reglas, y no
Markdown; queda abierto con qué modelo.

## Operaciones

### Texto sin store

| Operación | Anillo | Efecto | sldb.api | CLI | serve | mcp | Marcas |
|---|---|---|---|---|---|---|---|
| text_extract | 0a | lee | `extract_payload` | `extract` | `GET /extract` | — | |
| text_render | 0a | lee | — | `render` | `GET /render` | — | hueco: api |
| text_roundtrip_check | 0a | lee | — | `validate` | — | — | hueco: api; renombre (la CLI dice validate y lo que comprueba es la ida y vuelta) |

### Documentos

| Operación | Anillo | Efecto | sldb.api | CLI | serve | mcp | Marcas |
|---|---|---|---|---|---|---|---|
| documents_create | 0b | escribe | `create_document` | `docs create`, `doc add` | `POST /docs`, `POST /docs/create` | — | dup (cli: `doc add` es alias oculto → retirar; serve: dos rutas) |
| documents_track | 0b | escribe | `track_document_file` | `docs track`, `doc track` | `POST /docs/track` | — | dup (alias oculto) |
| documents_update | 0b | escribe | `save_document_payload` | `docs update`, `doc update` | `POST /save` | — | dup (alias oculto); renombre (save, update) |
| documents_untrack | 0b | escribe | `untrack_document` | `docs untrack`, `doc untrack` | `POST /docs/untrack` | — | dup (alias oculto) |
| documents_delete | 0b | escribe | `delete_document` | `docs delete` | — | — | |
| documents_read | 0b | lee | `runtime_document`, `extract_document_payload`, `render_document_markdown` | `docs show` | `GET /document` | `read_document` | dup (api: tres formatos de la misma lectura) |
| documents_list | 0b | lee | `load_runtime_documents` | `docs list` | — | — | reemplazo → documents_select sin selector |
| documents_select | 0b | lee | `select_documents` | `docs select` | `GET /docs/select` | `select_documents` | |
| documents_exists | 0b | lee | `doc_exists`, `doc_status`, `tracked_documents` | `docs exists` | — | — | dup (api) |
| documents_replace_text | 0b | escribe | `replace_text` | `docs replace` | — | — | |
| documents_move | 0b | externo | `move_document`, `move_path` | `move` | — | — | dup (api: un documento y una ruta cualquiera) |
| documents_ast | 0b | lee | `document_ast` | `ast show` | `GET /ast`, `GET /document/ir` | — | dup (serve) |
| documents_links_resolve | 0b | lee | — | `docs recover`, `legacy recover`, `recover` | — | — | dup (cli: tres nombres); reemplazo → edges_read cuando los enlaces del texto entren al índice de aristas (hoy no entran) |
| documents_history | 1 | lee | — | `docs history` | — | — | hueco: api |
| documents_compose | 3 | lee | — | `docs compose`, `legacy compose`, `compose` | — | — | dup (cli: tres nombres); hueco: api |
| documents_segments | 3 | lee | `build_document_segments` | — | `GET /document/segments`, `POST /extract/segments` | — | dup (serve); hueco: cli |

### Cambios en lote

| Operación | Anillo | Efecto | sldb.api | CLI | serve | mcp | Marcas |
|---|---|---|---|---|---|---|---|
| changes_propose | 1 | lee | — | — | — | `propose_changes` | hueco: cli; en la API es changes_apply con dry_run |
| changes_apply | 1 | escribe | `apply_batch`, `apply_batches`, `transaction` | — | — | `apply_changes` | hueco: cli |
| changes_undo | 1 | escribe | `undo_batches` | — | — | `undo_changes` | hueco: cli |

### Valores de un documento

| Operación | Anillo | Efecto | sldb.api | CLI | serve | mcp | Marcas |
|---|---|---|---|---|---|---|---|
| fields_read | 0b | lee | — | `fields show` | `GET /fields` | — | hueco: api (es documents_read con una ruta); `fields show models/…` lee el esquema, que es models_fields_read |
| fields_set | 0b | escribe | — | `fields create`, `fields update` | — | — | dup (dos verbos para escribir un valor); hueco: api (pasa por documents_update) |
| fields_remove | 0b | escribe | — | `fields remove` | — | — | hueco: api |
| fields_list_edit | 0b | escribe | — | `fields append`, `fields clean` | — | — | dup (dos verbos sobre una lista); reemplazo → fields_set con modo |
| fields_query | 0b | lee | — | `fields query` | — | — | reemplazo → documents_select con predicado |

### Secciones

| Operación | Anillo | Efecto | sldb.api | CLI | serve | mcp | Marcas |
|---|---|---|---|---|---|---|---|
| sections_read | 0b | lee | — | `sections show`, `sections fields` | `GET /sections` | — | hueco: api |
| sections_find | 0b | lee | — | `sections find` | — | — | reemplazo → search |

### Navegación y búsqueda

| Operación | Anillo | Efecto | sldb.api | CLI | serve | mcp | Marcas |
|---|---|---|---|---|---|---|---|
| search | 0b | lee | `search`, `where_matches` | `find`, `legacy find`, `raw-find` | `GET /find` | — | dup (cli: tres nombres) |
| addresses_read | 0b | lee | — | `legacy ls`, `legacy get`, `legacy glob`, `ls`, `get`, `glob` | — | — | dup; retirar: la gramática `st.{Model}.doc.field` la cubren documents_read, fields_read y documents_select |
| repo_text_search | 3 | lee | — | `explore`, `docs explore` | — | — | dup; reemplazo → search (busca además en docstrings y en los docs del repo, fuera del store) |
| ast_schema | 0b | lee | — | `ast schema` | — | — | hueco: api |

### Modelos

| Operación | Anillo | Efecto | sldb.api | CLI | serve | mcp | Marcas |
|---|---|---|---|---|---|---|---|
| models_create | 0b | externo | `create_model` | `models create` | `POST /models/create` | — | escribe el archivo Python del modelo |
| models_register | 0b | escribe | `add_model` | `models add`, `model add` | — | — | dup (alias oculto); renombre (add, register) |
| models_reindex | 0b | escribe | `reindex_model` | `models update`, `model update` | — | — | dup (alias oculto); renombre (update, reindex) |
| models_remove | 0b | escribe | `remove_model` | `models remove` | — | — | |
| models_list | 0b | lee | `registered_models` | `models list` | `GET /models` | `list_models` | |
| models_read | 0b | lee | `describe_model` | `models show` | `GET /models/detail` | `describe_model` | renombre (show, detail, describe) |
| models_check | 1 | lee | `is_model_registered` | `models check` | — | — | |
| models_fields_read | 0b | lee | `describe_field`, `describe_model_fields` | — | `GET /schema` | — | hueco: cli (hoy es `fields show models/…`) |
| models_fields_add | 0b | externo | `add_model_field` | `models fields add` | `POST /models/fields-add` | — | escribe el borrador del modelo |
| models_fields_remove | 0b | externo | `remove_model_field` | `models fields remove` | `POST /models/fields-remove` | — | escribe el borrador del modelo |
| models_template_read | 0b | lee | `render_model_template`, `template_anchors` | `models template show` | — | — | |
| models_template_edit | 0b | externo | `edit_model_template` | `models template edit` | `POST /models/template-edit` | — | escribe el borrador del modelo |
| models_metadata_edit | 0b | externo | `edit_model_metadata` | `models metadata edit` | `POST /models/metadata-edit` | — | escribe el borrador del modelo |
| models_validate | 1 | lee | `validate_model_draft` | `models validate` | `POST /models/validate` | — | |
| models_promote | 1 | externo | `promote_model_draft` | — | `POST /models/promote` | — | hueco: cli |
| models_inherit | 2 | escribe | `inherit_model` | `models inherit` | — | — | |

### Predicados de enlace

Hay tres vocabularios para el tipo de un enlace (nota de inbox del 2026-11-26): estos
predicados, `RelationTypeDoc` y los atributos del modelo. Propuesta: uno solo; toda esta
sección quedaría como `relation_types_*`.

| Operación | Anillo | Efecto | sldb.api | CLI | serve | mcp | Marcas |
|---|---|---|---|---|---|---|---|
| predicates_create | 0b | escribe | — | `predicates add` | — | — | hueco: api; reemplazo → relation_types |
| predicates_list | 0b | lee | — | `predicates list` | — | — | hueco: api; reemplazo → relation_types_list |
| predicates_read | 0b | lee | — | `predicates show` | — | — | hueco: api; reemplazo → relation_types_read |
| predicates_validate | 1 | lee | — | `predicates validate` | — | — | hueco: api; reemplazo → relation_types |
| predicates_delete | 0b | escribe | — | `predicates remove` | — | — | hueco: api; reemplazo → relation_types |
| predicates_sync | 0b | escribe | — | `predicates sync` | — | — | hueco: api; reemplazo → relation_types |
| predicates_export | 0b | externo | — | `predicates export` | — | — | hueco: api; reemplazo → relation_types |

### Aristas, nodos y tipos de relación

| Operación | Anillo | Efecto | sldb.api | CLI | serve | mcp | Marcas |
|---|---|---|---|---|---|---|---|
| relation_types_init | 0b | escribe | `init_relations` | `edges init` | — | — | |
| relation_types_list | 0b | lee | — | — | — | `list_relation_types` | hueco: api, cli |
| relation_types_read | 0b | lee | — | — | — | `describe_relation_type` | hueco: api, cli |
| edges_read | 0b | lee | `edges_from`, `edges_to` | `edges show` | `GET /edges` | `neighbors` | renombre (show, neighbors) |
| edges_referrers | 0b | lee | `referrers` | `edges referrers` | `GET /edges/referrers` | — | |
| edges_unresolved | 1 | lee | `unresolved_references` | `edges unresolved` | — | — | |
| edges_rewrite | 0b | escribe | `rewrite_references` | `edges rewrite` | `POST /edges/rewrite` | — | |
| edges_rebuild | 1 | escribe | `rebuild_edges` | `edges rebuild` | — | — | |
| edges_check | 1 | lee | `check_edges` | `edges check` | — | — | |
| nodes_read | 0b | lee | `edge_node` | `graph get` | `GET /edges/node` | — | renombre (graph, edges) |
| nodes_list | 0b | lee | `edge_nodes_of_type` | `graph list` | `GET /edges/nodes` | — | renombre (graph, edges) |
| transitions_evaluate | 1 | lee | `edges_holding`, `edges_blocked`, `effects_of`, `apply_effects`, `transition_findings` | — | — | — | hueco: cli |

### Análisis del grafo

| Operación | Anillo | Efecto | sldb.api | CLI | serve | mcp | Marcas |
|---|---|---|---|---|---|---|---|
| graph_neighborhood | 3 | lee | — | `graph neighborhood` | `GET /graph/neighborhood` | `neighborhood` | hueco: api |
| graph_path | 3 | lee | — | `graph path` | `GET /graph/path` | — | hueco: api |
| graph_cycles | 3 | lee | — | `graph cycles` | `GET /graph/cycles` | — | hueco: api |
| graph_order | 3 | lee | — | `graph order` | — | — | hueco: api |
| graph_components | 3 | lee | — | `graph components` | `GET /graph/components`, `GET /graph/isolated` | — | hueco: api; dup (serve: lo aislado es parte de components) |
| graph_central | 3 | lee | — | `graph central` | `GET /graph/central` | — | hueco: api |
| graph_similar | 3 | lee | — | `graph similar` | `GET /similar` | — | hueco: api |
| graph_query | 3 | lee | — | `graph query` | — | — | hueco: api; solapa con search: dos lenguajes de consulta |
| graph_snapshot_save | 3 | lee | `load_edge_index` | `graph snapshot save` | `GET /graph` | — | renombre (`GET /graph` da documentos y aristas para una interfaz) |
| graph_snapshot_load | 3 | lee | — | `graph snapshot load` | — | — | hueco: api |
| graph_ingest_semantic_export | 3 | lee | — | `graph ingest-sldb` | — | — | reemplazo → semantic_export con salida node-link |
| corpus_rank | 3 | lee | — | — | `GET /corpus/rank` | — | hueco: api, cli (la API expone el tipo `Corpus`, no la operación) |

### Grafo de proyecto

| Operación | Anillo | Efecto | sldb.api | CLI | serve | mcp | Marcas |
|---|---|---|---|---|---|---|---|
| project_graph_nodes | 3 | lee | `project_graph` | `graph project nodes` | `GET /project-graph/nodes` | — | |
| project_graph_edges | 3 | lee | — | `graph project edges` | `GET /project-graph/edges` | — | hueco: api; solapa con edges_read (otro grafo, la misma pregunta) |
| project_graph_missing | 3 | lee | — | `graph project missing` | `GET /project-graph/missing` | — | hueco: api; reemplazo → edges_unresolved |

### Reglas, anclas y salud

| Operación | Anillo | Efecto | sldb.api | CLI | serve | mcp | Marcas |
|---|---|---|---|---|---|---|---|
| rules_check | 1 | lee | `rules_check`, `rules_on_check`, `on_check_findings` | `rules check` | — | — | |
| rules_explain | 1 | lee | `rules_explain` | `rules explain` | — | — | |
| tags_check | 1 | lee | `tag_check`, `tag_evaluations` | `tags check` | — | — | reemplazo → rules_check filtrado por la familia `builtin:tag_namespace:*` |
| links_lint | 1 | lee | — | `lint` | `GET /lint` | — | hueco: api |
| anchors_record | 1 | escribe | — | `anchors record` | — | — | hueco: api; escribe solo con `--write` |
| anchors_check | 1 | lee | `check_doc_anchors` | `anchors check` | — | — | escribe con `--record` |
| anchors_resolve | 1 | lee | `anchors_resolve` | — | — | `anchors_resolve` | hueco: cli |

### Tags y DAG semántico

| Operación | Anillo | Efecto | sldb.api | CLI | serve | mcp | Marcas |
|---|---|---|---|---|---|---|---|
| tags_parent_add | 0b | escribe | `add_semantic_parent` | `semantic parent add` | — | — | |
| tags_parent_remove | 0b | escribe | `remove_semantic_parent` | `semantic parent remove` | — | — | |
| tags_equivalent_add | 2 | escribe | `add_semantic_equivalence` | `semantic equivalent add`, `stores semantic-map`, `store semantic-map` | — | — | dup (misma forma, dos conceptos; a confirmar que hacen lo mismo); hueco: borrar una equivalencia |
| tags_read | 0b | lee | `semantic_tag` | `semantic show` | — | — | renombre (semantic, tag) |
| tags_namespaces | 0b | lee | `tag_namespaces` | `tags namespaces` | — | — | |
| tags_tree | 0b | lee | `tag_tree` | `tags tree` | — | — | |
| semantic_export | 2 | lee | — | `stores semantic-export` | `GET /semantic-export` | — | hueco: api |

### Store

| Operación | Anillo | Efecto | sldb.api | CLI | serve | mcp | Marcas |
|---|---|---|---|---|---|---|---|
| stores_init | 2 | escribe | `init_store` | `stores init`, `store init` | — | — | dup (alias oculto) |
| stores_link | 2 | escribe | `link_store` | `stores add`, `store add` | — | — | dup (alias oculto); renombre (add, link) |
| stores_unlink | 2 | escribe | `unlink_store` | `stores remove` | — | — | renombre (remove, unlink) |
| stores_links_list | 2 | lee | `store_links` | `stores list` | `GET /stores` | — | |
| stores_check | 2 | lee | `check_store` | `stores check`, `store check` | `GET /stores/check` | `check_integrity` | dup (alias oculto); escribe con `--apply` |
| stores_update | 2 | escribe | `update_store_indexes` | `stores update`, `store update` | — | — | dup (alias oculto) |
| stores_rebuild_index | 2 | escribe | — | `stores rebuild-index` | — | — | hueco: api; solapa con stores_update (todo contra lo que cambió) |
| stores_fingerprint | 2 | lee | `store_fingerprint` | — | — | — | hueco: cli |
| stores_declare | 2 | lee | — | `stores declare` | — | — | hueco: api |
| stores_build | 2 | escribe | `build_store` | `stores build` | — | — | |
| stores_scaffold | 2 | externo | `scaffold_store` | `stores scaffold` | — | — | |
| stores_reconcile | 2 | externo | — | `stores reconcile` | — | — | hueco: api; escribe el catálogo global |
| stores_merge_driver | 2 | externo | — | `stores merge-driver` | — | — | hueco: api; lo llama git |
| stores_migrate_hashes | 2 | escribe | `migrate_store_hash_names` | `stores migrate-hashes` | — | — | retirar si ningún store lo necesita ya |
| stores_migrate_layout | 2 | escribe | `store_is_prepared` | `stores migrate-layout` | — | — | retirar si ningún store lo necesita ya |

### Notaciones y vistas

Hay dos clases de vista con el mismo nombre: las compuestas (`views`) y las de proyección
(`notations`, `/views/projection`). El MCP ya las sirve juntas con `list_views` y
`resolve_view`; la propuesta es que las demás caras hagan lo mismo.

| Operación | Anillo | Efecto | sldb.api | CLI | serve | mcp | Marcas |
|---|---|---|---|---|---|---|---|
| notations_list | 3 | lee | — | `notations list` | `GET /notations` | — | hueco: api; la CLI lista también vistas de proyección |
| notations_sync | 3 | escribe | `sync_notation`, `sync_palette` | `notations sync` | — | — | |
| notations_validate | 3 | lee | — | `notations validate` | — | — | hueco: api |
| notations_from_graph | 3 | lee | — | `notations from-graph` | — | — | hueco: api |
| notations_resolve_documents | 3 | lee | `resolve_documents` | `notations resolve` | `POST /notations/resolve` | — | |
| views_list | 3 | lee | `list_views`, `list_projection_views` | `views list` | `GET /views`, `GET /views/projection` | `list_views` | dup (dos clases de vista) |
| views_resolve | 3 | lee | `run_view`, `evaluate_projection_view`, `resolve_view` | `views run`, `notations view` | `GET /views/{name}`, `GET /views/projection/evaluate`, `POST /views/projection/evaluate`, `GET /notations/view` | `resolve_view` | dup (tres clases de vista); renombre (run, evaluate, view, resolve) |
| views_save | 3 | escribe | `save_projection_view` | — | `POST /views/projection/save` | — | hueco: cli |

### Documentación generada del código

| Operación | Anillo | Efecto | sldb.api | CLI | serve | mcp | Marcas |
|---|---|---|---|---|---|---|---|
| selfdoc_scan | 3 | lee | — | `selfdoc scan`, `selfdoc python-scan` | — | — | dup (dos fuentes, un verbo: propuesta, una opción de fuente) |
| selfdoc_sync | 3 | escribe | — | `selfdoc sync`, `selfdoc python-sync` | — | — | dup (ídem) |
| selfdoc_check | 3 | lee | — | `selfdoc check`, `selfdoc python-check` | — | — | dup (ídem) |

## Sin operación

| Nombres | Cara | Motivo |
|---|---|---|
| `help`, `faq` | cli | ayuda |
| `init`, `example` | cli | arranque: escriben un archivo de skill o el ejemplo, no tocan un store |
| `inbox` | cli | escribe en `desk/inbox/`, que es de deskops (`deskops message send`): retirar |
| `bench` | cli | herramienta de desarrollo que mide sldb y deskops: va a `tools/` |
| `serve`, `mcp` | cli | levantan una cara |
| `journal show`, `journal verify` | cli | retirados el 2026-11-04; solo imprimen el aviso: retirar |
| `journal`, `verify_journal` | api | retirados el 2026-11-04: retirar |
| `GET /health` | serve | estado del servidor |
| `list_signals` | mcp | los avisos de cambio que recibió el servidor MCP: son de la cara |
| `field_id`, `split_field_id`, `anchor_node_id`, `bare`, `doc_node_id`, `field_node_id`, `kind`, `model_node_id`, `relation_type_node_id`, `section_node_id`, `tag_node_id` | api | construir o partir identificadores |
| `deep_get`, `deep_set`, `deep_delete`, `ensure_list`, `leaf_paths` | api | rutas dentro de un payload en memoria |
| `serialize_document`, `serialize_edge_node_records`, `serialize_edge_records` | api | serializar para una cara |
| `open_store`, `read_store`, `load_registered_model`, `resolve_model_ref`, `locate_model_source`, `resolve_indexed_document`, `indexed_model_bases`, `split_doc_ref`, `refuse_unknown_family`, `tag_folder` | api | resolución interna que usan las operaciones |
| `Segment` | api | alias de tipo |
| `Corpus`, `CorpusEntry`, `FieldEntry`, `FieldHit`, `FieldProjection`, `Hit`, `IndexProjection`, `CompositionPiece`, `CompositionSpec`, `DocumentSegments`, `FieldSegment`, `LiteralSegment`, `SourceRef`, `DocumentHashes`, `DocumentReference`, `DraftDocumentCheck`, `DraftValidationReport`, `EdgeCheckReport`, `EdgeIndex`, `EdgeNodeRecord`, `EdgeRebuildReport`, `EdgeRecord`, `FieldDecl`, `FieldDescription`, `JournalEntry`, `JournalVerifyReport`, `LinkedStore`, `ModelCheck`, `ModelDescription`, `ModelDocumentSummary`, `ModelDraft`, `ModelFieldSummary`, `ModelRegistration`, `ModelSource`, `RegisteredModel`, `RelationsInitReport`, `StoreFingerprint`, `StoreLocation`, `StoreUpdateReport`, `RuntimeDocuments`, `InvalidDocument`, `AmbiguousSelectionError`, `Selector`, `DocRefStatus`, `AmbiguousDocument`, `WherePredicateError`, `StructuredNLDoc`, `UnresolvedReference`, `BatchReport`, `ConflictError`, `RollbackError`, `Transaction`, `NothingToUndo`, `UndoReport`, `MovePathReport`, `ScaffoldReport`, `Seed`, `StoreDeclaration`, `ProjectGraph`, `ProjectGraphConfig`, `Referrer`, `RewriteReport`, `GlyphDoc`, `LinkDoc`, `NotationDoc`, `PaletteDoc`, `SpecDoc`, `SpecNodeDoc`, `ViewDoc`, `TagNamespace` | api | tipos de dato, reportes y excepciones de las operaciones |

## Lo que la tabla deja ver

- **La CLI pasa de 151 comandos hoja a unos 120 sin perder nada**: salen los 17 alias ocultos,
  el grupo `legacy`, `journal`, las dos migraciones si ya no hacen falta, `inbox` y `bench`.
  Con los reemplazos propuestos (búsquedas, predicados, vistas, `fields`) quedan unos 100.
- **La navegación tiene más de diez entradas** (`find`, `explore`, `fields query`,
  `sections find`, `graph query`, `legacy`, `docs select`, …). El eje 4 de JP pide una.
- **El anillo 1 no tiene verbo propio**: revisar está repartido entre `stores check`,
  `edges check`, `rules check`, `tags check`, `models check`, `anchors check`, `lint` y
  `docs recover`.
- **El análisis del grafo no está en la API**: la CLI y `serve` lo calculan cada una por su
  lado.
- **Escribir en lote solo existe en el MCP** (`propose_changes`, `apply_changes`,
  `undo_changes`); la CLI no puede proponer, aplicar un lote ni deshacer.
- **Faltan celdas del eje 1**: borrar un store, cambiar un campo de modelo, crear o borrar una
  sección o un tag, borrar una equivalencia semántica.

## Abierto

- Que JP apruebe los nombres canónicos y las marcas de reemplazo.
- Con qué modelo del store queda la tabla cuando se apruebe.
- La gramática de direcciones (ADR [One Address Grammar](one-address-grammar-two-spaces.md),
  borrador): cambia los argumentos de casi todas las filas, no las filas.
