# Command Taxonomy: One Row Per Operation

- Status: Proposed; waiting for the owner's approval (step 1 of
  [One Command Taxonomy, Served By FastMCP](one-command-taxonomy-served-by-fastmcp.md))
- Date: 2026-11-25
- Kept complete by: `tests/test_command_taxonomy.py`

An inventory, not a change: no code was renamed, moved or removed. It reconciles the four faces
of sldb (`sldb.api`, the CLI, `sldb serve`, `sldb mcp`) in one table: each operation with a noun,
a verb, whether it reads or writes, its permission level, the name it has today in each face and
a canonical name proposed. Duplicates, gaps and renames are marked.

## What is reused

- **`SurfaceDoc` and `CmdDoc` (`knowledge/surfaces/`, `knowledge/commands/`) and `sldb selfdoc`**
  already register the CLI face: one `CmdDoc` per visible leaf command (134, the same 134 that
  `Operaciones` cites) and one `SurfaceDoc` per group, filled from `build_parser` by
  `sldb selfdoc sync` and checked by `sldb selfdoc check`. They are cited here as the source of
  the CLI column and are not modified. They hold **no** `sldb.api` name, route or MCP tool, no
  noun/verb, no permission level and no marks, so they cannot hold this taxonomy as they are.
  Whether they could is the open question of the ADR and is not answered here.
- **The code** is the source of every name (see *How the names are read*); the document is the
  reviewable view of it and the test is what keeps the two equal.
- Nothing else is new: this is one Markdown table and one test, because no existing piece records
  the four faces side by side.

## How the names are read

| Face | Rule | Count today |
|---|---|---|
| `sldb.api` | each name in `sldb.api.__all__` | 192 |
| CLI | each argparse leaf (a subcommand with no subcommands of its own); aliases of one parser count once; hidden leaves (suppressed help, in the `hidden.py`/`legacy.py` parsers) go to *Sin operación* | 151 (134 visible, 17 hidden) |
| `sldb serve` | each route path literal under `src/sldb/cli/serve/`, plus the `/views/<name>` family that `views_routes.py` parses by prefix; no static files and no `/openapi.json` (the server has none). `POST /docs` exists and is listed | 56 paths |
| `sldb mcp` | each tool `sldb.mcp.registry` registers (`READ_TOOLS`, `list_signals`, three write tools); extension tools are not part of sldb | 15 |

A route that answers both `GET` and `POST` shares one path and is written `GET,POST /path`.
The test compares paths; methods are as read in the code on 2026-11-25.

Columns of *Operaciones*:

- **Operación**: the proposed canonical name, `noun_verb` in snake_case. Where a face already uses
  a name that fits (`rules_check`, `edges_show`...) that name is kept; ties go to the `sldb.api`
  name.
- **Acceso**: `lee` or `escribe` (the operation changes something).
- **Permiso**: `lee`; `escribe-store` (changes the store, even if it also reads); `efecto-externo`
  (git, network, processes or files outside the store). It maps onto the MCP levels 0, 1 and 2 of
  [`sldb mcp`](mcp.md) only in part: level 2 (rules as data) is a matter of *which* documents a
  write touches, not of the operation, and is not decided here.
- **Marcas**: `duplicado` (a face has more than one name for it), `renombre` (the `sldb.api` or MCP
  name differs from the canonical one; CLI and routes are paths, so they always differ and do not
  count), `hueco: faces` (the faces that do not offer it).

## Reading the table

- 142 operations; 130 names with no operation (109 api, 21 cli, 0 serve, 0 mcp).
- Faces that offer an operation: api 70, CLI 126, serve 55, mcp 15 of 142.
- 16 operations with more than one name in a face; 74 with an api or MCP name different from the canonical one.
- 47 operations exist only in the CLI. 10 routes have no CLI command and 6 MCP tools have no `sldb.api` name of their own (their code does the work with other api calls).
- 72 operations have no `sldb.api` name at all (empty `sldb.api` cell): the CLI or a route does
  the work through lower layers. Those are the gaps a single FastMCP server would have to close first.

## Operaciones

| Operación | Sustantivo | Verbo | Acceso | Permiso | sldb.api | CLI | sldb serve | sldb mcp | Marcas |
|---|---|---|---|---|---|---|---|---|---|
| `stores_init` | stores | init | escribe | escribe-store | `init_store` | `stores init` | — | — | renombre, hueco: serve, mcp |
| `stores_link` | stores | link | escribe | escribe-store | `link_store` | `stores add` | — | — | renombre, hueco: serve, mcp |
| `stores_unlink` | stores | unlink | escribe | escribe-store | `unlink_store` | `stores remove` | — | — | renombre, hueco: serve, mcp |
| `stores_list` | stores | list | lee | lee | `store_links` | `stores list` | `GET /stores` | — | renombre, hueco: mcp |
| `stores_check` | stores | check | lee | lee | `check_store` | `stores check` | `GET /stores/check` | `check_integrity` | renombre; mcp `check_integrity` suma el índice de aristas (`edges_check`) |
| `stores_update` | stores | update | escribe | escribe-store | `update_store_indexes` | `stores update` | — | — | renombre, hueco: serve, mcp |
| `stores_reconcile` | stores | reconcile | escribe | escribe-store | — | `stores reconcile` | — | — | hueco: api, serve, mcp |
| `stores_semantic_export` | stores | semantic_export | lee | lee | — | `stores semantic-export` | `GET /semantic-export` | — | hueco: api, mcp |
| `stores_migrate_hashes` | stores | migrate_hashes | escribe | escribe-store | `migrate_store_hash_names` | `stores migrate-hashes` | — | — | renombre, hueco: serve, mcp |
| `stores_migrate_layout` | stores | migrate_layout | escribe | escribe-store | — | `stores migrate-layout` | — | — | hueco: api, serve, mcp |
| `stores_declare` | stores | declare | lee | lee | — | `stores declare` | — | — | hueco: api, serve, mcp |
| `stores_build` | stores | build | escribe | escribe-store | `build_store` | `stores build` | — | — | renombre, hueco: serve, mcp |
| `stores_scaffold` | stores | scaffold | escribe | escribe-store | `scaffold_store` | `stores scaffold` | — | — | renombre, hueco: serve, mcp |
| `stores_rebuild_index` | stores | rebuild_index | escribe | escribe-store | — | `stores rebuild-index` | — | — | hueco: api, serve, mcp |
| `stores_merge_driver` | stores | merge_driver | escribe | efecto-externo | — | `stores merge-driver` | — | — | hueco: api, serve, mcp |
| `store_health` | store | health | lee | lee | — | — | `GET /health` | — | hueco: api, cli, mcp |
| `schema_describe` | schema | describe | lee | lee | — | — | `GET /schema` | — | hueco: api, cli, mcp |
| `models_register` | models | register | escribe | escribe-store | `add_model` | `models add` | — | — | renombre, hueco: serve, mcp |
| `models_reindex` | models | reindex | escribe | escribe-store | `reindex_model` | `models update` | — | — | renombre, hueco: serve, mcp |
| `models_unregister` | models | unregister | escribe | escribe-store | `remove_model` | `models remove` | — | — | renombre, hueco: serve, mcp |
| `models_inherit` | models | inherit | escribe | escribe-store | `inherit_model` | `models inherit` | — | — | renombre, hueco: serve, mcp |
| `models_list` | models | list | lee | lee | `registered_models` | `models list` | `GET /models` | `list_models` | renombre |
| `models_describe` | models | describe | lee | lee | `describe_model`<br>`describe_model_fields`<br>`describe_field` | `models show` | `GET /models/detail` | `describe_model` | duplicado, renombre; tres nombres públicos para describir un modelo y sus campos |
| `models_exists` | models | exists | lee | lee | `is_model_registered` | `models check` | — | — | renombre, hueco: serve, mcp |
| `models_validate` | models | validate | lee | lee | `validate_model_draft` | `models validate` | `POST /models/validate` | — | renombre, hueco: mcp |
| `models_promote` | models | promote | escribe | escribe-store | `promote_model_draft` | — | `POST /models/promote` | — | renombre, hueco: cli, mcp; la CLI no ofrece `promote` |
| `models_create` | models | create | escribe | escribe-store | `create_model` | `models create` | `POST /models/create` | — | renombre, hueco: mcp |
| `models_template_show` | models | template_show | lee | lee | — | `models template show` | — | — | hueco: api, serve, mcp |
| `models_template_edit` | models | template_edit | escribe | escribe-store | `edit_model_template` | `models template edit` | `POST /models/template-edit` | — | renombre, hueco: mcp |
| `models_field_add` | models | field_add | escribe | escribe-store | `add_model_field` | `models fields add` | `POST /models/fields-add` | — | renombre, hueco: mcp |
| `models_field_remove` | models | field_remove | escribe | escribe-store | `remove_model_field` | `models fields remove` | `POST /models/fields-remove` | — | renombre, hueco: mcp |
| `models_metadata_edit` | models | metadata_edit | escribe | escribe-store | `edit_model_metadata` | `models metadata edit` | `POST /models/metadata-edit` | — | renombre, hueco: mcp |
| `predicates_add` | predicates | add | escribe | escribe-store | — | `predicates add` | — | — | hueco: api, serve, mcp |
| `predicates_list` | predicates | list | lee | lee | — | `predicates list` | — | — | hueco: api, serve, mcp |
| `predicates_show` | predicates | show | lee | lee | — | `predicates show` | — | — | hueco: api, serve, mcp |
| `predicates_validate` | predicates | validate | lee | lee | — | `predicates validate` | — | — | hueco: api, serve, mcp |
| `predicates_remove` | predicates | remove | escribe | escribe-store | — | `predicates remove` | — | — | hueco: api, serve, mcp |
| `predicates_sync` | predicates | sync | escribe | escribe-store | — | `predicates sync` | — | — | hueco: api, serve, mcp |
| `predicates_export` | predicates | export | escribe | efecto-externo | — | `predicates export` | — | — | hueco: api, serve, mcp |
| `rules_check` | rules | check | lee | lee | `rules_check` | `rules check` | — | — | hueco: serve, mcp |
| `rules_explain` | rules | explain | lee | lee | `rules_explain` | `rules explain` | — | — | hueco: serve, mcp |
| `documents_create` | documents | create | escribe | escribe-store | `create_document` | `docs create` | `POST /docs`<br>`POST /docs/create` | — | duplicado, renombre, hueco: mcp; `POST /docs` es la cara compacta de `POST /docs/create` |
| `documents_track` | documents | track | escribe | escribe-store | `track_document_file` | `docs track` | `POST /docs/track` | — | renombre, hueco: mcp |
| `documents_untrack` | documents | untrack | escribe | escribe-store | `untrack_document` | `docs untrack` | `POST /docs/untrack` | — | renombre, hueco: mcp |
| `documents_delete` | documents | delete | escribe | escribe-store | `delete_document` | `docs delete` | — | — | renombre, hueco: serve, mcp |
| `documents_update` | documents | update | escribe | escribe-store | `save_document_payload` | `docs update` | `POST /save` | — | renombre, hueco: mcp; `POST /save` escribe uno o varios documentos con `expected` (lote) |
| `documents_show` | documents | show | lee | lee | `runtime_document`<br>`serialize_document` | `docs show` | `GET /document` | `read_document` | duplicado, renombre; `ast show` entrega el AST del mismo documento (`ast_show`) |
| `documents_exists` | documents | exists | lee | lee | `doc_exists`<br>`doc_status` | `docs exists` | — | — | duplicado, renombre, hueco: serve, mcp |
| `documents_list` | documents | list | lee | lee | `tracked_documents` | `docs list` | — | — | renombre, hueco: serve, mcp |
| `documents_select` | documents | select | lee | lee | `select_documents` | `docs select` | `GET /docs/select` | `select_documents` | renombre |
| `documents_history` | documents | history | lee | lee | — | `docs history` | — | — | hueco: api, serve, mcp |
| `documents_replace_text` | documents | replace_text | escribe | escribe-store | `replace_text` | `docs replace` | — | — | renombre, hueco: serve, mcp |
| `documents_move` | documents | move | escribe | efecto-externo | `move_document`<br>`move_path` | `move` | — | — | duplicado, renombre, hueco: serve, mcp; git mv más reescritura de campos y enlaces |
| `documents_recover_links` | documents | recover_links | lee | lee | — | `docs recover`<br>`legacy recover` | — | — | duplicado, hueco: api, serve, mcp; `legacy recover` duplica a `docs recover`; el oculto `recover` también |
| `documents_compose` | documents | compose | lee | lee | `build_document_segments` | `docs compose`<br>`legacy compose` | `GET /document/segments` | — | duplicado, renombre, hueco: mcp; `legacy compose` duplica a `docs compose` |
| `documents_explore` | documents | explore | lee | lee | — | `docs explore`<br>`explore` | — | — | duplicado, hueco: api, serve, mcp; `explore` (raíz) duplica a `docs explore` |
| `documents_segments_extract` | documents | segments_extract | lee | lee | — | — | `POST /extract/segments` | — | hueco: api, cli, mcp |
| `documents_ir_show` | documents | ir_show | lee | lee | — | — | `GET /document/ir` | — | hueco: api, cli, mcp |
| `changes_propose` | changes | propose | lee | lee | — | — | — | `propose_changes` | renombre, hueco: api, cli, serve; no escribe: sella un lote con `expected_source_hash` |
| `changes_apply` | changes | apply | escribe | escribe-store | `apply_batch`<br>`apply_batches`<br>`transaction` | — | — | `apply_changes` | duplicado, renombre, hueco: cli, serve |
| `changes_undo` | changes | undo | escribe | escribe-store | — | — | — | `undo_changes` | renombre, hueco: api, cli, serve; solo en la sesión; el inverso sale de `BatchReport.inverse` |
| `markdown_extract` | markdown | extract | lee | lee | `extract_payload`<br>`extract_document_payload` | `extract` | `GET /extract` | — | duplicado, renombre, hueco: mcp |
| `markdown_render` | markdown | render | lee | lee | `render_document_markdown`<br>`render_model_template` | `render` | `GET /render` | — | duplicado, renombre, hueco: mcp |
| `markdown_validate` | markdown | validate | lee | lee | — | `validate` | — | — | hueco: api, serve, mcp; comprueba idempotencia extract→render |
| `fields_show` | fields | show | lee | lee | — | `fields show` | `GET /fields` | — | hueco: api, mcp |
| `fields_query` | fields | query | lee | lee | — | `fields query` | — | — | hueco: api, serve, mcp |
| `fields_create` | fields | create | escribe | escribe-store | — | `fields create` | — | — | hueco: api, serve, mcp |
| `fields_update` | fields | update | escribe | escribe-store | — | `fields update` | — | — | hueco: api, serve, mcp |
| `fields_remove` | fields | remove | escribe | escribe-store | — | `fields remove` | — | — | hueco: api, serve, mcp |
| `fields_append` | fields | append | escribe | escribe-store | — | `fields append` | — | — | hueco: api, serve, mcp |
| `fields_clean` | fields | clean | escribe | escribe-store | — | `fields clean` | — | — | hueco: api, serve, mcp |
| `sections_show` | sections | show | lee | lee | — | `sections show` | `GET /sections` | — | hueco: api, mcp |
| `sections_find` | sections | find | lee | lee | — | `sections find` | — | — | hueco: api, serve, mcp |
| `sections_fields` | sections | fields | lee | lee | — | `sections fields` | — | — | hueco: api, serve, mcp |
| `corpus_search` | corpus | search | lee | lee | `search` | `find` | `GET /find` | — | renombre, hueco: mcp; `GET /corpus/rank` ordena por similitud (`corpus_rank`) |
| `corpus_rank` | corpus | rank | lee | lee | — | — | `GET /corpus/rank` | — | hueco: api, cli, mcp |
| `ast_show` | ast | show | lee | lee | `document_ast` | `ast show` | `GET /ast` | — | renombre, hueco: mcp |
| `ast_schema` | ast | schema | lee | lee | — | `ast schema` | — | — | hueco: api, serve, mcp |
| `references_lint` | references | lint | lee | lee | — | `lint` | `GET /lint` | — | hueco: api, mcp |
| `edges_init` | edges | init | escribe | escribe-store | `init_relations` | `edges init` | — | — | renombre, hueco: serve, mcp |
| `edges_rebuild` | edges | rebuild | escribe | escribe-store | `rebuild_edges` | `edges rebuild` | — | — | renombre, hueco: serve, mcp |
| `edges_check` | edges | check | lee | lee | `check_edges` | `edges check` | — | — | renombre, hueco: serve, mcp |
| `edges_show` | edges | show | lee | lee | `edges_from`<br>`edges_to` | `edges show` | `GET /edges` | `neighbors` | duplicado, renombre; mcp `neighbors` es la lectura directa; `neighborhood` es `graph_neighborhood` |
| `edges_unresolved` | edges | unresolved | lee | lee | `unresolved_references` | `edges unresolved` | — | — | renombre, hueco: serve, mcp |
| `edges_referrers` | edges | referrers | lee | lee | `referrers` | `edges referrers` | `GET /edges/referrers` | — | renombre, hueco: mcp |
| `edges_rewrite` | edges | rewrite | escribe | escribe-store | `rewrite_references` | `edges rewrite` | `POST /edges/rewrite` | — | renombre, hueco: mcp |
| `relation_types_list` | relation_types | list | lee | lee | — | — | — | `list_relation_types` | renombre, hueco: api, cli, serve |
| `relation_types_describe` | relation_types | describe | lee | lee | — | — | — | `describe_relation_type` | renombre, hueco: api, cli, serve |
| `graph_node_get` | graph | node_get | lee | lee | `edge_node` | `graph get` | `GET /edges/node` | — | renombre, hueco: mcp |
| `graph_node_list` | graph | node_list | lee | lee | `edge_nodes_of_type` | `graph list` | `GET /edges/nodes` | — | renombre, hueco: mcp; `graph list` lista ids; la ruta y `edge_nodes_of_type` filtran por tipo |
| `graph_query` | graph | query | lee | lee | — | `graph query` | — | — | hueco: api, serve, mcp |
| `graph_neighborhood` | graph | neighborhood | lee | lee | — | `graph neighborhood` | `GET /graph/neighborhood` | `neighborhood` | renombre, hueco: api |
| `graph_path` | graph | path | lee | lee | — | `graph path` | `GET /graph/path` | — | hueco: api, mcp |
| `graph_cycles` | graph | cycles | lee | lee | — | `graph cycles` | `GET /graph/cycles` | — | hueco: api, mcp |
| `graph_order` | graph | order | lee | lee | — | `graph order` | — | — | hueco: api, serve, mcp |
| `graph_components` | graph | components | lee | lee | — | `graph components` | `GET /graph/components` | — | hueco: api, mcp |
| `graph_central` | graph | central | lee | lee | — | `graph central` | `GET /graph/central` | — | hueco: api, mcp |
| `graph_isolated` | graph | isolated | lee | lee | — | — | `GET /graph/isolated` | — | hueco: api, cli, mcp |
| `graph_similar` | graph | similar | lee | lee | — | `graph similar` | `GET /similar` | — | hueco: api, mcp; `GET /similar` llama a `graph_similar` de `sldb.api.graph.analyze`, que no es público |
| `graph_snapshot_save` | graph | snapshot_save | escribe | efecto-externo | — | `graph snapshot save` | `GET /graph` | — | hueco: api, mcp; `GET /graph` sirve el mismo índice de aristas sin escribir archivo |
| `graph_snapshot_load` | graph | snapshot_load | lee | lee | — | `graph snapshot load` | — | — | hueco: api, serve, mcp |
| `graph_ingest_sldb` | graph | ingest_sldb | lee | lee | — | `graph ingest-sldb` | — | — | hueco: api, serve, mcp |
| `project_graph_nodes` | project_graph | nodes | lee | lee | `project_graph` | `graph project nodes` | `GET /project-graph/nodes` | — | renombre, hueco: mcp; `project_graph` sirve a las tres operaciones `project_graph_*` |
| `project_graph_edges` | project_graph | edges | lee | lee | — | `graph project edges` | `GET /project-graph/edges` | — | hueco: api, mcp |
| `project_graph_missing` | project_graph | missing | lee | lee | — | `graph project missing` | `GET /project-graph/missing` | — | hueco: api, mcp |
| `journal_show` | journal | show | lee | lee | `journal` | `journal show` | — | — | renombre, hueco: serve, mcp; retirado: imprime el aviso y sale 0 |
| `journal_verify` | journal | verify | lee | lee | `verify_journal` | `journal verify` | — | — | renombre, hueco: serve, mcp; retirado: imprime el aviso y sale 0 |
| `semantic_parent_add` | semantic | parent_add | escribe | escribe-store | `add_semantic_parent` | `semantic parent add` | — | — | renombre, hueco: serve, mcp |
| `semantic_parent_remove` | semantic | parent_remove | escribe | escribe-store | `remove_semantic_parent` | `semantic parent remove` | — | — | renombre, hueco: serve, mcp |
| `semantic_equivalent_add` | semantic | equivalent_add | escribe | escribe-store | `add_semantic_equivalence` | `semantic equivalent add`<br>`stores semantic-map` | — | — | duplicado, renombre, hueco: serve, mcp; `stores semantic-map` repite `semantic equivalent add` con otro nombre |
| `semantic_show` | semantic | show | lee | lee | `semantic_tag` | `semantic show` | — | — | renombre, hueco: serve, mcp |
| `anchors_record` | anchors | record | lee | lee | — | `anchors record` | — | — | hueco: api, serve, mcp |
| `anchors_check` | anchors | check | lee | lee | `check_doc_anchors` | `anchors check` | — | — | renombre, hueco: serve, mcp |
| `tags_namespaces` | tags | namespaces | lee | lee | `tag_namespaces` | `tags namespaces` | — | — | renombre, hueco: serve, mcp |
| `tags_tree` | tags | tree | lee | lee | `tag_tree`<br>`tag_folder` | `tags tree` | — | — | duplicado, renombre, hueco: serve, mcp |
| `tags_check` | tags | check | lee | lee | `tag_check`<br>`tag_evaluations` | `tags check` | — | — | duplicado, renombre, hueco: serve, mcp |
| `notations_list` | notations | list | lee | lee | — | `notations list` | `GET /notations` | — | hueco: api, mcp |
| `notations_sync` | notations | sync | escribe | escribe-store | `sync_notation`<br>`sync_palette` | `notations sync` | — | — | duplicado, renombre, hueco: serve, mcp |
| `notations_validate` | notations | validate | lee | lee | — | `notations validate` | — | — | hueco: api, serve, mcp |
| `notations_view` | notations | view | lee | lee | `resolve_view` | `notations view` | `GET /notations/view` | `resolve_view` | renombre |
| `notations_resolve` | notations | resolve | lee | lee | `resolve_documents` | `notations resolve` | `POST /notations/resolve` | — | renombre, hueco: mcp |
| `notations_from_graph` | notations | from_graph | lee | lee | — | `notations from-graph` | — | — | hueco: api, serve, mcp |
| `views_list` | views | list | lee | lee | `list_views` | `views list` | `GET /views` | `list_views` | renombre |
| `views_run` | views | run | lee | lee | `run_view` | `views run` | `GET /views/<name>` | — | renombre, hueco: mcp; mcp `resolve_view` resuelve también SpecDoc y ViewDoc de proyección (ver `notations_view`) |
| `projection_views_list` | projection_views | list | lee | lee | `list_projection_views` | — | `GET /views/projection` | — | renombre, hueco: cli, mcp |
| `projection_views_evaluate` | projection_views | evaluate | lee | lee | `evaluate_projection_view` | — | `GET,POST /views/projection/evaluate` | — | renombre, hueco: cli, mcp |
| `projection_views_save` | projection_views | save | escribe | escribe-store | `save_projection_view` | — | `POST /views/projection/save` | — | renombre, hueco: cli, mcp |
| `skill_init` | skill | init | escribe | efecto-externo | — | `init` | — | — | hueco: api, serve, mcp |
| `example_unpack` | example | unpack | escribe | efecto-externo | — | `example` | — | — | hueco: api, serve, mcp |
| `inbox_log` | inbox | log | escribe | efecto-externo | — | `inbox` | — | — | hueco: api, serve, mcp |
| `bench_run` | bench | run | escribe | efecto-externo | — | `bench` | — | — | hueco: api, serve, mcp |
| `selfdoc_scan` | selfdoc | scan | lee | lee | — | `selfdoc scan` | — | — | hueco: api, serve, mcp |
| `selfdoc_sync` | selfdoc | sync | escribe | escribe-store | — | `selfdoc sync` | — | — | hueco: api, serve, mcp |
| `selfdoc_check` | selfdoc | check | lee | lee | — | `selfdoc check` | — | — | hueco: api, serve, mcp |
| `selfdoc_python_scan` | selfdoc | python_scan | lee | lee | — | `selfdoc python-scan` | — | — | hueco: api, serve, mcp |
| `selfdoc_python_sync` | selfdoc | python_sync | escribe | escribe-store | — | `selfdoc python-sync` | — | — | hueco: api, serve, mcp |
| `selfdoc_python_check` | selfdoc | python_check | lee | lee | — | `selfdoc python-check` | — | — | hueco: api, serve, mcp |
| `signals_list` | signals | list | lee | lee | — | — | — | `list_signals` | renombre, hueco: api, cli, serve |
| `legacy_ls` | legacy | ls | lee | lee | — | `legacy ls` | — | — | hueco: api, serve, mcp; duplica el comando oculto `ls` |
| `legacy_get` | legacy | get | lee | lee | — | `legacy get` | — | — | hueco: api, serve, mcp; duplica el comando oculto `get` |
| `legacy_glob` | legacy | glob | lee | lee | — | `legacy glob` | — | — | hueco: api, serve, mcp; duplica el comando oculto `glob` |
| `legacy_find` | legacy | find | lee | lee | — | `legacy find` | — | — | hueco: api, serve, mcp; duplica el comando oculto `raw-find` |

## Sin operación

A name that is an alias, help, a launcher, a data type or an internal utility is not an operation.
Each one is listed once with its reason. Types and exceptions are not repeated by name in prose.

| Cara | Nombre | Motivo |
|---|---|---|
| api | `AmbiguousDocument` | tipo de datos o excepción, no operación |
| api | `AmbiguousSelectionError` | tipo de datos o excepción, no operación |
| api | `BatchReport` | tipo de datos o excepción, no operación |
| api | `CompositionPiece` | tipo de datos o excepción, no operación |
| api | `CompositionSpec` | tipo de datos o excepción, no operación |
| api | `ConflictError` | tipo de datos o excepción, no operación |
| api | `Corpus` | tipo de datos o excepción, no operación |
| api | `CorpusEntry` | tipo de datos o excepción, no operación |
| api | `DocRefStatus` | tipo de datos o excepción, no operación |
| api | `DocumentHashes` | tipo de datos o excepción, no operación |
| api | `DocumentReference` | tipo de datos o excepción, no operación |
| api | `DocumentSegments` | tipo de datos o excepción, no operación |
| api | `DraftDocumentCheck` | tipo de datos o excepción, no operación |
| api | `DraftValidationReport` | tipo de datos o excepción, no operación |
| api | `EdgeCheckReport` | tipo de datos o excepción, no operación |
| api | `EdgeIndex` | tipo de datos o excepción, no operación |
| api | `EdgeNodeRecord` | tipo de datos o excepción, no operación |
| api | `EdgeRebuildReport` | tipo de datos o excepción, no operación |
| api | `EdgeRecord` | tipo de datos o excepción, no operación |
| api | `FieldDecl` | tipo de datos o excepción, no operación |
| api | `FieldDescription` | tipo de datos o excepción, no operación |
| api | `FieldEntry` | tipo de datos o excepción, no operación |
| api | `FieldHit` | tipo de datos o excepción, no operación |
| api | `FieldProjection` | tipo de datos o excepción, no operación |
| api | `FieldSegment` | tipo de datos o excepción, no operación |
| api | `GlyphDoc` | tipo de datos o excepción, no operación |
| api | `Hit` | tipo de datos o excepción, no operación |
| api | `IndexProjection` | tipo de datos o excepción, no operación |
| api | `InvalidDocument` | tipo de datos o excepción, no operación |
| api | `JournalEntry` | tipo de datos o excepción, no operación |
| api | `JournalVerifyReport` | tipo de datos o excepción, no operación |
| api | `LinkDoc` | tipo de datos o excepción, no operación |
| api | `LinkedStore` | tipo de datos o excepción, no operación |
| api | `LiteralSegment` | tipo de datos o excepción, no operación |
| api | `ModelCheck` | tipo de datos o excepción, no operación |
| api | `ModelDescription` | tipo de datos o excepción, no operación |
| api | `ModelDocumentSummary` | tipo de datos o excepción, no operación |
| api | `ModelDraft` | tipo de datos o excepción, no operación |
| api | `ModelFieldSummary` | tipo de datos o excepción, no operación |
| api | `ModelRegistration` | tipo de datos o excepción, no operación |
| api | `ModelSource` | tipo de datos o excepción, no operación |
| api | `MovePathReport` | tipo de datos o excepción, no operación |
| api | `NotationDoc` | tipo de datos o excepción, no operación |
| api | `PaletteDoc` | tipo de datos o excepción, no operación |
| api | `ProjectGraph` | tipo de datos o excepción, no operación |
| api | `ProjectGraphConfig` | tipo de datos o excepción, no operación |
| api | `Referrer` | tipo de datos o excepción, no operación |
| api | `RegisteredModel` | tipo de datos o excepción, no operación |
| api | `RelationsInitReport` | tipo de datos o excepción, no operación |
| api | `RewriteReport` | tipo de datos o excepción, no operación |
| api | `RollbackError` | tipo de datos o excepción, no operación |
| api | `RuntimeDocuments` | tipo de datos o excepción, no operación |
| api | `ScaffoldReport` | tipo de datos o excepción, no operación |
| api | `Seed` | tipo de datos o excepción, no operación |
| api | `Segment` | alias de tipo (unión de segmentos) |
| api | `Selector` | tipo de datos o excepción, no operación |
| api | `SourceRef` | tipo de datos o excepción, no operación |
| api | `SpecDoc` | tipo de datos o excepción, no operación |
| api | `SpecNodeDoc` | tipo de datos o excepción, no operación |
| api | `StoreDeclaration` | tipo de datos o excepción, no operación |
| api | `StoreFingerprint` | tipo de datos o excepción, no operación |
| api | `StoreLocation` | tipo de datos o excepción, no operación |
| api | `StoreUpdateReport` | tipo de datos o excepción, no operación |
| api | `StructuredNLDoc` | tipo de datos o excepción, no operación |
| api | `TagNamespace` | tipo de datos o excepción, no operación |
| api | `Transaction` | tipo de datos o excepción, no operación |
| api | `UnresolvedReference` | tipo de datos o excepción, no operación |
| api | `ViewDoc` | tipo de datos o excepción, no operación |
| api | `WherePredicateError` | tipo de datos o excepción, no operación |
| api | `anchor_node_id` | utilidad interna: id de nodo del grafo |
| api | `apply_effects` | utilidad interna: efectos de transición de aristas |
| api | `bare` | utilidad interna: id de nodo del grafo |
| api | `deep_delete` | utilidad interna: borrado por ruta de payload |
| api | `deep_get` | utilidad interna: lectura por ruta de payload |
| api | `deep_set` | utilidad interna: escritura por ruta de payload |
| api | `doc_node_id` | utilidad interna: id de nodo del grafo |
| api | `edges_blocked` | utilidad interna: predicado de transición |
| api | `edges_holding` | utilidad interna: predicado de transición |
| api | `effects_of` | utilidad interna: efectos de transición de aristas |
| api | `ensure_list` | utilidad interna: normaliza a lista |
| api | `field_id` | utilidad interna: arma el id de un campo |
| api | `field_node_id` | utilidad interna: id de nodo del grafo |
| api | `indexed_model_bases` | utilidad interna: bases de modelos indexados |
| api | `kind` | utilidad interna: id de nodo del grafo |
| api | `leaf_paths` | utilidad interna: rutas de hojas de un payload |
| api | `load_edge_index` | utilidad interna: carga el índice de aristas |
| api | `load_registered_model` | utilidad interna: carga un modelo registrado |
| api | `load_runtime_documents` | utilidad interna: carga documentos de runtime |
| api | `locate_model_source` | utilidad interna: ubica el fuente de un modelo |
| api | `model_node_id` | utilidad interna: id de nodo del grafo |
| api | `on_check_findings` | utilidad interna: hallazgos de reglas en check |
| api | `open_store` | utilidad interna: abre la tienda |
| api | `read_store` | utilidad interna: lee el índice de la tienda |
| api | `refuse_unknown_family` | utilidad interna: guarda de escritura de reglas |
| api | `relation_type_node_id` | utilidad interna: id de nodo del grafo |
| api | `resolve_indexed_document` | utilidad interna: resuelve una referencia de documento |
| api | `resolve_model_ref` | utilidad interna: resuelve la referencia a un modelo |
| api | `rules_on_check` | utilidad interna: reglas en check |
| api | `section_node_id` | utilidad interna: id de nodo del grafo |
| api | `serialize_edge_node_records` | utilidad interna: serialización de nodos |
| api | `serialize_edge_records` | utilidad interna: serialización de aristas |
| api | `split_doc_ref` | utilidad interna: parte una referencia de documento |
| api | `split_field_id` | utilidad interna: parte el id de un campo |
| api | `store_fingerprint` | utilidad interna: huella de la tienda |
| api | `store_is_prepared` | utilidad interna: predicado de preparación |
| api | `tag_node_id` | utilidad interna: id de nodo del grafo |
| api | `template_anchors` | utilidad interna: anclas de plantilla |
| api | `transition_findings` | utilidad interna: hallazgos de reglas en transición |
| api | `where_matches` | utilidad interna: predicado `where` |
| cli | `help` | ayuda: texto curado de la CLI |
| cli | `faq` | ayuda: preguntas frecuentes |
| cli | `serve` | arranca la cara HTTP, no es operación sobre la tienda |
| cli | `mcp` | arranca la cara MCP, no es operación sobre la tienda |
| cli | `store init` | alias oculto de `stores init` |
| cli | `store add` | alias oculto de `stores add` |
| cli | `store check` | alias oculto de `stores check` |
| cli | `store update` | alias oculto de `stores update` |
| cli | `store semantic-map` | alias oculto de `stores semantic-map` |
| cli | `model add` | alias oculto de `models add` |
| cli | `model update` | alias oculto de `models update` |
| cli | `doc add` | alias oculto de `docs create` |
| cli | `doc track` | alias oculto de `docs track` |
| cli | `doc update` | alias oculto de `docs update` |
| cli | `doc untrack` | alias oculto de `docs untrack` |
| cli | `ls` | oculto: consulta cruda, duplicado de `legacy ls` |
| cli | `get` | oculto: consulta cruda, duplicado de `legacy get` |
| cli | `glob` | oculto: consulta cruda, duplicado de `legacy glob` |
| cli | `raw-find` | oculto: consulta cruda, duplicado de `legacy find` |
| cli | `recover` | oculto: duplicado de `legacy recover` |
| cli | `compose` | oculto: duplicado de `legacy compose` |

## Decisions for the owner

1. The canonical names, above all the nouns: `documents` (CLI `docs`), `stores` vs `store` (the
   hidden singular groups are aliases), `edges` vs `graph`, `markdown_*` for `extract`/`render`.
2. The three permission values and where `efecto-externo` ends: `graph_snapshot_save` and
   `predicates_export` write a file outside the store; `documents_move` runs `git mv`.
3. What happens to the 16 duplicated operations: keep one name per face, or keep both
   during the migration. The old routes stay until both interfaces migrate (ADR).
4. Which `hueco` closes first. The ADR names extraction, render, lint, AST, similarity and
   notations as missing from MCP; the table gives the full list, per operation.
5. Operations to retire rather than rename: `journal_show`, `journal_verify` (already retired,
   exit 0), the hidden aliases and `legacy_*`.

Approval is the owner's and is not part of this inventory.

