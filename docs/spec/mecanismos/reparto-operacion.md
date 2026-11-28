# Mecanismo: reparto del bloque operación

Clase de página: mecanismo. Fecha: 2026-11-27. Estado: **propuesta de un agente, sin revisar**.
No se movió código: es un análisis hecho leyendo cada archivo (docstring, nombres públicos e imports)
y buscando sus usos con grep. Sigue a `modulos.md`, sección "Lo que sigue".

Alcance: los siete ejes de `contracts/layers.toml` que forman "operación", resueltos con
`tools/check_axes.py` en modo lectura. Son **372 archivos**:

| Eje | Archivos |
|---|---|
| op_almacen | 100 |
| op_documentos | 89 |
| op_aristas | 76 |
| op_modelos | 59 |
| reglas | 23 |
| vistas_compuestas | 13 |
| anclaje | 12 |

Las rutas son relativas a `src/sldb/`. Las frases de cada archivo son la primera línea de su
docstring (en inglés, como está en el código), recortada. Cada archivo tiene un solo destino; los
que hacen dos cosas están además en la sección "Partir".

## Resumen

Cada archivo llega a un módulo por lo que hace, no por dónde está. Las filas "NUEVO" son grupos de
archivos que no calzan en ningún módulo de `modulos.md` (ver "Sin módulo").

| Módulo destino | op_documentos | op_modelos | op_aristas | op_almacen | anclaje | reglas | vistas_compuestas | Total |
|---|---|---|---|---|---|---|---|---|
| Datos (kernel) | 8 | 0 | 4 | 20 | 0 | 0 | 0 | 32 |
| Consultas y reglas (kernel) | 2 | 0 | 1 | 12 | 0 | 0 | 0 | 15 |
| Árboles (kernel) | 3 | 0 | 0 | 7 | 3 | 0 | 0 | 13 |
| Anclaje (kernel) | 1 | 0 | 0 | 0 | 8 | 0 | 0 | 9 |
| Interfaz con git (kernel) | 1 | 0 | 0 | 2 | 0 | 0 | 0 | 3 |
| Documentos con forma | 25 | 6 | 0 | 0 | 0 | 0 | 0 | 31 |
| Operaciones sobre documentos, modelos y relaciones | 28 | 17 | 14 | 0 | 0 | 0 | 0 | 59 |
| Semántica | 0 | 0 | 0 | 1 | 1 | 7 | 0 | 9 |
| Reglas, estados y política de escritura | 5 | 0 | 2 | 5 | 0 | 16 | 0 | 28 |
| Análisis del grafo | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 5 |
| Notaciones y vistas | 0 | 0 | 0 | 0 | 0 | 0 | 13 | 13 |
| Similitud | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Varios stores y migración | 0 | 5 | 0 | 11 | 0 | 0 | 0 | 16 |
| Lo que se hace con git encima | 2 | 0 | 0 | 8 | 0 | 0 | 0 | 10 |
| NUEVO: Referencias del proyecto | 0 | 0 | 50 | 0 | 0 | 0 | 0 | 50 |
| NUEVO: Diagnóstico del store | 0 | 0 | 0 | 20 | 0 | 0 | 0 | 20 |
| NUEVO: Declaración y montaje del store | 0 | 0 | 0 | 14 | 0 | 0 | 0 | 14 |
| NUEVO: Escritura por lotes y transacciones | 14 | 0 | 0 | 0 | 0 | 0 | 0 | 14 |
| NUEVO: Contratos de modelo (editar el código del modelo) | 0 | 31 | 0 | 0 | 0 | 0 | 0 | 31 |
| **Total** | 89 | 59 | 76 | 100 | 12 | 23 | 13 | 372 |

En cifras: al kernel van 72 archivos (Datos 32, Consultas 15, Árboles 13, Anclaje 9, Interfaz con
git 3). A librerías ya listadas van 171 (Operaciones 59, Documentos con forma 31, Reglas 28,
Varios stores 16, Notaciones y vistas 13, git encima 10, Semántica 9, Análisis del grafo 5).
A cinco módulos candidatos nuevos van 129. 72 + 171 + 129 = 372. Similitud y Código a documentos
no reciben ningún archivo entero (Similitud recibe una función suelta, ver "Partir").

## Archivos por módulo destino

Los módulos del kernel primero, luego las librerías, luego los candidatos nuevos.

### Datos (kernel) (32)

- `api/documents/content_hash.py` (op_documentos): The hash of what a document says, apart from who signed it and when: its text without the
- `api/documents/doc_hashes.py` (op_documentos): The hashes the store holds for a tracked document.
- `api/stores/__init__.py` (op_almacen): Store operations: open, link and refresh the indexes of a store.
- `api/stores/ambiguous_document.py` (op_almacen): More than one submodel of the asked model tracks a document with that name.
- `api/stores/document_field_hashes.py` (op_almacen): Extract a document once and sign both its payload and each field of it.
- `api/stores/index_commit.py` (op_almacen): Save refreshed model indexes and rebuild the derived store indexes under the store lock.
- `api/stores/index_refresh.py` (op_almacen): Rehash every tracked document of a store whose Markdown changed since it was indexed.
- `api/stores/indexed_documents.py` (op_almacen): The documents a store tracks, read from its indexes alone.
- `api/stores/init_store.py` (op_almacen): Create a new, empty store in a project directory.
- `api/stores/open_store.py` (op_almacen): Open a store: resolve where it lives and start a fresh sldb operation over it.
- `api/stores/read_store.py` (op_almacen): Read a store without migrating it: a fresh read-only operation over a prepared store.
- `api/stores/rebuild_index.py` (op_almacen): `sldb stores rebuild-index`: `core/store_index.yaml` and `core/models/*.yaml` regenerated
- `api/stores/resolve_indexed_document.py` (op_almacen): Find a tracked document by `Model:name`, where Model may be a base of the document's model.
- `api/stores/store_discovery.py` (op_almacen): Resolve a store argument (a path, a linked-store alias or nothing) to a `.sldb` directory.
- `api/stores/store_fingerprint.py` (op_almacen): The store's Merkle tree as one public value (spec 14 C10/D6).
- `api/stores/store_location.py` (op_almacen): The resolved location of one sldb store, as returned by `open_store`.
- `api/stores/store_skeleton.py` (op_almacen): Write the empty indexes of a new store and register it in the global catalog.
- `api/stores/store_update_report.py` (op_almacen): Outcome of refreshing a store's indexes, as returned by `update_store_indexes`.
- `api/stores/update_store_indexes.py` (op_almacen): Refresh a store's indexes after its Markdown documents were edited outside sldb.
- `store/documents_dirty.py` (op_documentos): Per-model, per-namespace dirty tracking for `documents_hash`'s `note`/`forget` (PLAN 15
- `store/documents_dirty_persist.py` (op_documentos): The dirty-document sets of `documents_dirty`, kept in `<store>/../.sldb_cache/documents_dirty.json`
- `store/edge_doc_contribution.py` (op_aristas): One document's edges shard (the sections pattern, PLAN 15 capa 5): the shard, keyed by
- `store/edge_rebuild.py` (op_aristas): The edge index brought current (mirror of section_rebuild; the typed ingest itself lives
- `store/edge_sync.py` (op_aristas): Bringing one model's edges shards current (mirror of section_sync): skipped whole when the
- `store/export.py` (op_almacen): The `sldb_kgdb_semantic_export` payload, built from the persisted indexes.
- `store/field_set_drift.py` (op_almacen): A document signed under another field set: its per-field hashes name a field the model no
- `store/model_node.py` (op_aristas): Stamp a model's node and its two children onto its index, in one place.
- `store/ops.py` (op_almacen): (sin docstring) define StoreOperations, track_document, cascade_store_hash
- `store/section_doc_contribution.py` (op_documentos): One document's sections shard (PLAN 15 capa 5): the shard, keyed by `source_hash`, is the
- `store/section_paths.py` (op_documentos): Deterministic path allocation for persisted Markdown sections.
- `store/section_rebuild.py` (op_documentos): (sin docstring) define rebuild_sections_indexes
- `store/section_sync.py` (op_documentos): Bringing one model's sections shards current (PLAN 15 capa 5): skipped whole when the

### Consultas y reglas (kernel) (15)

- `api/documents/select_documents.py` (op_documentos): `select_documents`: which tracked documents a selector names, as the library answers it.
- `api/documents/selector.py` (op_documentos): The selector of `select_documents`: a mapping of keys combined by conjunction.
- `api/graph/execute.py` (op_aristas): Run structured queries and read nodes from a store's edge index.
- `api/records/__init__.py` (op_almacen): Record-level reads: the store seen as searchable store/model/doc/section/field records.
- `api/records/fields.py` (op_almacen): (sin docstring) define query_field_records
- `api/records/iter_records.py` (op_almacen): (sin docstring) define iter_search_records
- `api/records/iter_records_docs.py` (op_almacen): (vacío)
- `api/records/iter_records_helpers.py` (op_almacen): (vacío)
- `api/records/matches.py` (op_almacen): (sin docstring) define search_records
- `api/records/record_filters.py` (op_almacen): (sin docstring) define RecordFilters
- `api/records/record_serialization.py` (op_almacen): Serialization of search records: the shape `sldb find --format json` emits.
- `api/records/resolve.py` (op_almacen): (sin docstring) define resolve_runtime_doc
- `api/records/runtime_doc_proxy.py` (op_almacen): (sin docstring) define RuntimeDocProxy
- `api/records/search_record.py` (op_almacen): (sin docstring) define SearchRecord
- `api/records/section_record.py` (op_almacen): (sin docstring) define SectionRecord

### Árboles (kernel) (13)

- `api/code/__init__.py` (anclaje): Code facts as a public API: what `sldb.code` reads from Python, TS, TSX, JS, JSX and SQL.
- `api/code/code_facts.py` (anclaje): `code_facts`: the facts of a file, a directory or the whole tree, through `sldb.code.scan`.
- `api/code/requested_files.py` (anclaje): The files a `code_facts` call reads: the requested paths checked against `root`, directories expanded.
- `api/documents/document_ast.py` (op_documentos): One document's normalized tree: the CLI `ast show docs/<doc>` surface, api-side.
- `api/documents/document_ir_serialization.py` (op_documentos): JSON projection of a document's IR: serialization lives here, not in the serve transport.
- `api/documents/heading_scan.py` (op_documentos): Read the headings out of a Markdown string, as (level, title) pairs.
- `api/records/ast_target.py` (op_almacen): (sin docstring) define ast_for_target
- `api/records/build_ast.py` (op_almacen): (sin docstring) define build_store_ast
- `api/records/build_ir.py` (op_almacen): (sin docstring) define build_document_ir
- `api/records/extract.py` (op_almacen): (sin docstring) define extract_sections
- `api/records/flatten.py` (op_almacen): (sin docstring) define flatten_payload
- `api/records/map_fields.py` (op_almacen): (vacío)
- `api/records/utils.py` (op_almacen): (vacío)

### Anclaje (kernel) (9)

- `api/anchors/__init__.py` (anclaje): Code anchors (docs/architecture/code-anchoring.md): record what a symbol looks like, check
- `api/anchors/anchor_docs.py` (anclaje): The anchor documents of a store, and the two writes anchoring makes: a reconnection, and a
- `api/anchors/anchor_report.py` (anclaje): What `anchors check` says of one anchor, and the finding it becomes.
- `api/anchors/check_anchors.py` (anclaje): Every code anchor of a store against the code now (code-anchoring.md §4): read-only unless
- `api/anchors/check_doc_anchors.py` (anclaje): Every document anchor of a store against its target now (GO07, anchoring.md §6): one alert
- `api/anchors/reconnect.py` (anclaje): Where a symbol went when its name is gone (code-anchoring.md §5): selfdoc's rename heuristic
- `api/anchors/record_anchor.py` (anclaje): What a symbol looks like now: the `code` block an anchor keeps (code-anchoring.md §2).
- `api/anchors/resolve_pointers.py` (anclaje): Where a pointer lands (code-anchoring.md, tags.md): which documents cover a file or a symbol,
- `api/documents/doc_anchor_pinning.py` (op_documentos): Pinning on save (GO07, docs/architecture/anchoring.md §6): a `doc:Model:name` without

### Interfaz con git (kernel) (3)

- `api/documents/relocate_file.py` (op_documentos): Move a file on disk, through `git mv` when git versions it so git records a rename.
- `api/stores/branch_stores.py` (op_almacen): Other local branches of the same repository that already have a store at this path: the
- `api/stores/merge_driver_install.py` (op_almacen): `sldb stores merge-driver --install`: register the driver for this clone, idempotently.

### Documentos con forma (31)

- `api/documents/document_render.py` (op_documentos): Render and extract one document through its model, the wiki's path.
- `api/documents/extract_payload.py` (op_documentos): Extract a payload from Markdown already read, without touching any store.
- `api/documents/frontmatter_keys.py` (op_documentos): Find the frontmatter keys a document carries that its model never declares.
- `api/documents/rewrite_loss.py` (op_documentos): What a rewrite of a document would lose: its blocks that do not survive render(extract(text)).
- `api/documents/structural_noise.py` (op_documentos): Find the headings a document carries that its model's `__template__` never declares.
- `api/documents/structural_noise_report.py` (op_documentos): The verdict of a structural-noise scan, and the refusal message it renders.
- `api/model_registry/template_anchors.py` (op_modelos): The literal paragraph that anchors each field of a model's template.
- `api/schema/__init__.py` (op_modelos): Field schema: describe the fields of a model class for forms and schemas.
- `api/schema/describe_field.py` (op_modelos): Describe the fields of a model class for forms and schemas.
- `api/schema/field_description.py` (op_modelos): Moved to `sldb.models.field_schema.description`; re-exported here.
- `api/schema/store_schema.py` (op_modelos): Every registered model described, with the broken ones declared explicitly.
- `api/schema/unavailable_model.py` (op_modelos): A registered model that could not be described, and why.
- `api/segments/__init__.py` (op_documentos): Document segments: the boundary types for a document seen as editable spans.
- `api/segments/build_document_segments.py` (op_documentos): Build the ``DocumentSegments`` view of one tracked document.
- `api/segments/build_extraction_segments.py` (op_documentos): Locate a model's fields inside raw markdown that is not a tracked document.
- `api/segments/composition_piece.py` (op_documentos): One rendered piece of a composed field, traced back to its source document.
- `api/segments/composition_spec.py` (op_documentos): The composition declaration behind a ``render`` field that assembles pieces.
- `api/segments/document_segments.py` (op_documentos): A whole document seen as an editable sequence of literals and field spans.
- `api/segments/extract_markdown_segments.py` (op_documentos): Extract segments from raw markdown, naming a model registered in a store.
- `api/segments/extracted_field.py` (op_documentos): One field located in raw markdown, with how confidently it was placed.
- `api/segments/extraction_segments.py` (op_documentos): What a model finds in a piece of raw markdown, and what it leaves unexplained.
- `api/segments/field_ref_resolver.py` (op_documentos): Resolves field references against an SLDB store.
- `api/segments/field_segment.py` (op_documentos): A stretch of document text that one marker wrote out of the payload.
- `api/segments/literal_segment.py` (op_documentos): A stretch of document text that came from the template, not from a value.
- `api/segments/payload_values.py` (op_documentos): Read a field's typed value and kind out of a payload by segment path.
- `api/segments/segment.py` (op_documentos): The ``Segment`` union and the forward references that close it.
- `api/segments/segment_display.py` (op_documentos): Decide whether a field's surface owns its own block of the document.
- `api/segments/segment_enrichment.py` (op_documentos): Enriches document segments with views, projections, and table data.
- `api/segments/segment_nodes.py` (op_documentos): Turn one recorded span into the segment dict the contract describes.
- `api/segments/source_ref.py` (op_documentos): Where a segment's text came from when it is not the document's own payload.
- `api/segments/text_range.py` (op_documentos): A stretch of text addressed by character offsets.

### Operaciones sobre documentos, modelos y relaciones (59)

- `api/documents/__init__.py` (op_documentos): Document operations: track, untrack, save payloads and navigate payload paths.
- `api/documents/create_document.py` (op_documentos): Render a payload to a new Markdown file and track it as a document of a registered model.
- `api/documents/data_values.py` (op_documentos): Parse a value written as text (JSON first, YAML otherwise).
- `api/documents/delete_document.py` (op_documentos): Delete a tracked document: untrack it AND remove its Markdown file, leaving no residue.
- `api/documents/document_lookup.py` (op_documentos): Find a tracked document by name or path across a store's models.
- `api/documents/document_payload.py` (op_documentos): One tracked document's runtime record and payload addressing, api-side.
- `api/documents/document_reference.py` (op_documentos): A tracked document addressed by model and name, as returned by document operations.
- `api/documents/document_serialization.py` (op_documentos): JSON projection of a RuntimeDocument: the API contract serializers live here, not in the CLI.
- `api/documents/invalid_document.py` (op_documentos): A tracked document its model rejects, as ``load_runtime_documents(..., on_invalid="skip")`` names it.
- `api/documents/move_document.py` (op_documentos): Move a tracked document's Markdown file and keep it tracked under the same name.
- `api/documents/move_path.py` (op_documentos): Move a file or directory and keep the store and the repo's references to it true.
- `api/documents/move_path_apply.py` (op_documentos): Carry a `MovePlan` out inside a transaction: fields, then links, then the files themselves.
- `api/documents/move_path_fields.py` (op_documentos): The field values of tracked documents that name a moved path, rewritten in a copy of the payload.
- `api/documents/move_path_files.py` (op_documentos): The files a move touches and the Markdown files whose links it may rewrite.
- `api/documents/move_path_links.py` (op_documentos): Inline Markdown links (`[text](dest)`) to a moved path, pointed at its new place.
- `api/documents/move_path_plan.py` (op_documentos): Everything a move will do, worked out before anything is touched.
- `api/documents/move_path_remap.py` (op_documentos): What a moved path becomes: the old and new project-relative paths, and whether it is a directory.
- `api/documents/move_path_report.py` (op_documentos): What `move_path` moved and every reference it rewrote (or would, with `dry_run`).
- `api/documents/move_path_resolve.py` (op_documentos): The checks before a move: the path exists, the destination is free and stays inside the project.
- `api/documents/payload_diff.py` (op_documentos): The fields a document write changed, as dotted paths through two payloads.
- `api/documents/payload_path_reading.py` (op_documentos): Read a value inside a document payload by a dotted path (`items.0.name`).
- `api/documents/payload_path_writing.py` (op_documentos): Set or delete a value inside a document payload by a dotted path, in place.
- `api/documents/payload_save.py` (op_documentos): Write a whole payload back to a tracked document: render, round-trip, rehash, reindex.
- `api/documents/payload_save_steps.py` (op_documentos): The steps of `save_document_payload`, moved here from `sldb.cli.commands.fields_save`.
- `api/documents/replace_text.py` (op_documentos): `sldb.api.replace_text(store, ref, old, new, *, count=1, transaction=None)` (GD27): exactly
- `api/documents/runtime_documents.py` (op_documentos): Bulk runtime load through sldb.api: every tracked document, payload and both hashes.
- `api/documents/track_document_file.py` (op_documentos): Start tracking an existing Markdown file as a document of a registered model.
- `api/documents/untrack_document.py` (op_documentos): Stop tracking a document: drop it from the store indexes, leaving its Markdown file alone.
- `api/edges/__init__.py` (op_aristas): The edge index as a library: read edges and nodes, rebuild, check, and prepare a store for
- `api/edges/builtin_relation_writes.py` (op_aristas): Write the builtin relation types as tracked documents and register them as predicates.
- `api/edges/check_edges.py` (op_aristas): Validate every edge of a store's index against its relation type.
- `api/edges/document_edge.py` (op_aristas): One document-to-document edge, as a UI draws it.
- `api/edges/document_edges.py` (op_aristas): Every document-to-document edge of a store, current with its documents.
- `api/edges/edge_check_report.py` (op_aristas): Outcome of checking a store's edge index, as returned by `check_edges`.
- `api/edges/edge_evidence.py` (op_aristas): Edges with their evidence: the target's hash, the source's contract, and who derived them.
- `api/edges/edge_reading.py` (op_aristas): Read the edge index of a store: the one door to edges and nodes.
- `api/edges/edge_serialization.py` (op_aristas): JSON projections of edge-index records (pydantic models) for API consumers.
- `api/edges/init_relations.py` (op_aristas): Prepare a store for typed relations: the relation models, the builtin relation types.
- `api/edges/rebuild_edges.py` (op_aristas): Bring a store's edge index current.
- `api/edges/relation_models.py` (op_aristas): Register the two relation models in a store, or re-point a store that still registers them
- `api/edges/relations_init_report.py` (op_aristas): Outcome of preparing a store for typed relations, as returned by `init_relations`.
- `api/edges/unresolved_references.py` (op_aristas): The declared references of a store that name no document.
- `api/model_registry/__init__.py` (op_modelos): Model registry operations: resolve, register, reindex and describe models.
- `api/model_registry/add_model.py` (op_modelos): Register a model class in a store so documents of that model can be tracked.
- `api/model_registry/describe_model.py` (op_modelos): Describe one registered model: its registry record, its fields and its tracked documents.
- `api/model_registry/load_registered_model.py` (op_modelos): Look up a model registered in a store (or in a linked store) and import its class.
- `api/model_registry/model_class_attrs.py` (op_modelos): Class-level attributes and draft status of a registered model, for its description.
- `api/model_registry/model_description.py` (op_modelos): A registered model's contract and documents, as returned by `describe_model`.
- `api/model_registry/model_document_summary.py` (op_modelos): One tracked document of a registered model, as `describe_model` lists it.
- `api/model_registry/model_field_summary.py` (op_modelos): One field of a registered model, as `describe_model` lists it.
- `api/model_registry/model_files.py` (op_modelos): Every file a registered model owns in its store: its two indexes and its derived shards.
- `api/model_registry/model_index_writes.py` (op_modelos): Write the indexes of a newly registered model and of a reindexed one.
- `api/model_registry/model_lineage.py` (op_modelos): What a model class declares about its place in the model hierarchy.
- `api/model_registry/model_reference.py` (op_modelos): Import a model class from its `module:ClassName` reference.
- `api/model_registry/model_registration.py` (op_modelos): A model's registry record after registering or reindexing it.
- `api/model_registry/registered_model.py` (op_modelos): A model registered in a store, resolved to its class, as returned by `load_registered_model`.
- `api/model_registry/registration_query.py` (op_modelos): Which models a store has registered, asked without reading its index files.
- `api/model_registry/reindex_model.py` (op_modelos): Recompute a registered model's document hashes after its class or documents changed.
- `api/model_registry/remove_model.py` (op_modelos): Unregister a model (the inverse of `add_model`), with its documents only when asked.

### Semántica (9)

- `api/anchors/tag_reach.py` (anclaje): What a tag reaches in the semantic DAG: itself, everything below it, and the equivalents.
- `api/rules/builtin_tag_findings.py` (reglas): The findings of the built-in family `builtin:tag_namespace:*` (GD27) and the evaluations
- `api/rules/builtin_tag_rules.py` (reglas): The built-in rule family `builtin:tag_namespace:<name>` (GD27, docs/architecture/tags.md):
- `api/stores/tag_namespace.py` (op_almacen): One entry of `tag_namespaces` in `.sldb/store.yaml` (GD27, docs/architecture/tags.md).
- `api/tags/__init__.py` (reglas): Tag namespaces as the store declares them (GD27, docs/architecture/tags.md): the tree of a
- `api/tags/tag_check.py` (reglas): `sldb tags namespaces` and `sldb tags check`: what the store declares and what fails it.
- `api/tags/tag_evaluation.py` (reglas): The family `builtin:tag_namespace:*` as data (H6, docs/architecture/tags.md): per local
- `api/tags/tag_folder.py` (reglas): Where a tag places a document: `a.b` -> `a/b`, one segment per part (`folder_axis`).
- `api/tags/tag_tree.py` (reglas): `sldb.api.tag_tree(store, namespace)`: one namespace's tags as a tree (docs/architecture/tags.md).

### Reglas, estados y política de escritura (28)

- `api/actor.py` (op_documentos): Who is writing, for the `by` of every document's provenance block.
- `api/documents/lossy_overwrite.py` (op_documentos): The guard of a field write: it refuses to drop what the file carries and the model does not declare.
- `api/documents/on_write_gate.py` (op_documentos): H4: a document that enters the store (`create_document`, `track_document_file`) passes the
- `api/documents/provenance_stamp.py` (op_documentos): Sign a document's text on write: the `sldb` block with who, when, through what, with which authority.
- `api/documents/refuse_structural_noise.py` (op_documentos): The refusal every path that writes a new document goes through.
- `api/edges/apply_effects.py` (op_aristas): Apply an edge's effects to a subject, purely: the new payload, validated, never persisted.
- `api/edges/edge_effects.py` (op_aristas): An edge's effects on a subject: its `sets` with `{field}` filled from the subject, and `terminal`.
- `api/edges/edges_blocked.py` (reglas): Edges a subject's `on_transition` rules block (GO08, rules.md §9): the other half of
- `api/edges/edges_holding.py` (reglas): Edges whose condition holds for a subject: the graph read as a state machine.
- `api/rules/__init__.py` (reglas): Rules (GO06): the RuleDoc documents of a store, evaluated with the predicate language.
- `api/rules/dirty_set.py` (reglas): The dirty set of the rules cache (GO08, rules.md §9): `<.sldb_cache>/rules/dirty.json`.
- `api/rules/fixpoint.py` (reglas): Closures and the witness of a rule's finding (GO08 p3, rules.md §9).
- `api/rules/rule_cache.py` (reglas): The derived cache of the rules (GO08, rules.md §9): `<.sldb_cache>/rules/` of the store.
- `api/rules/rule_graph.py` (reglas): The store a rule is evaluated over: its edge index, loaded once into the store's
- `api/rules/rule_reach.py` (reglas): Whether a store's rules can read a linked store's document (rules.md §9, GO08): when they
- `api/rules/rule_subjects.py` (reglas): Which rules a store declares, which documents a rule applies to, and how a reference names one.
- `api/rules/rule_view.py` (reglas): The graph view a `RuleGraph` evaluates over, adjusted for a write: declared edges swapped in,
- `api/rules/rule_writes.py` (reglas): What writing a RuleDoc checks against the store: every `model <= X` of its subject names a
- `api/rules/rules_check.py` (reglas): `sldb rules check`: the local rules evaluated, each failure a core `Finding` (GO06).
- `api/rules/rules_explain.py` (reglas): `sldb rules explain RULE SUBJECT`: the eval finding of one rule on one document (GO06).
- `api/rules/rules_on_check.py` (reglas): `on_check` (GO08, rules.md §9): every `on_check` rule of the store, recomputed only where
- `api/rules/rules_on_transition.py` (reglas): `on_transition` (GO08, rules.md §9): the rules a transition of a document must pass.
- `api/rules/rules_on_write.py` (reglas): `on_write` (GO08, rules.md §9): the rules a write must pass before anything is persisted.
- `api/stores/apply_findings.py` (op_almacen): `sldb stores check --apply`: run what the policy answers to each finding.
- `api/stores/judge_findings.py` (op_almacen): Findings read through the store's policy (docs/architecture/provenance.md §5).
- `api/stores/policy.py` (op_almacen): How a store reads a finding: through the document's authority and its own declared policy
- `api/stores/policy_subject.py` (op_almacen): What a policy knows of the document a finding is about (docs/architecture/provenance.md §5).
- `store/package_version.py` (op_almacen): The real package version, for provenance stamps such as `producer.version`.

### Análisis del grafo (5)

- `api/graph/__init__.py` (op_aristas): The graph layer as a library: query, traverse, analyse, and the portable snapshot format.
- `api/graph/analyze.py` (op_aristas): Whole-graph analysis of a store: the questions that need more than one hop.
- `api/graph/neighborhood.py` (op_aristas): Neighborhood traversal over a store's edge index.
- `api/graph/snapshot.py` (op_aristas): Portable snapshot read/write and the ingest-sldb route.
- `api/graph/traverse.py` (op_aristas): Relation-parametrized walks over a store's edge index, as library functions.

### Notaciones y vistas (13)

- `api/views/__init__.py` (vistas_compuestas): Composed views (GD25): a `ViewDoc` with `sections` evaluated over a store.
- `api/views/list_views.py` (vistas_compuestas): The composed views a store holds (GD25, q11), and the loading of one ViewDoc by name.
- `api/views/run_view.py` (vistas_compuestas): `sldb.api.run_view(store, name, params)`: a composed ViewDoc evaluated (GD25).
- `api/views/view_edges.py` (vistas_compuestas): The neighbour ids a section's `edges` entry adds to a row (GD25, q8).
- `api/views/view_groups.py` (vistas_compuestas): Rows grouped by one field, in a declared order (GD25, q10).
- `api/views/view_links.py` (vistas_compuestas): Whether a view needs the linked stores' documents (H11): `run_view` composes the edge index of
- `api/views/view_nodes.py` (vistas_compuestas): The `ViewDoc` nodes of a store and of every store it links to (H9), read from the ViewDoc
- `api/views/view_reading.py` (vistas_compuestas): What one `run_view` evaluation reads, loaded once and shared by every section and row (H11:
- `api/views/view_revision.py` (vistas_compuestas): The revision of a view's result (GD25, q16): what changes when anything it read changes.
- `api/views/view_rows.py` (vistas_compuestas): The rows of a section: `select_documents` with `{param}` filled, each row with its projected fields.
- `api/views/view_rules.py` (vistas_compuestas): The findings a section's `rules` add to each row (GD25): the RuleDocs named, evaluated as
- `api/views/view_source.py` (vistas_compuestas): Which ViewDoc node a name means, and its file read from the store that tracks it (H9).
- `api/views/view_transitions.py` (vistas_compuestas): The `holding` and `blocked` edges a section's `transitions` add to each row (GD25): what

### Varios stores y migración (16)

- `api/model_registry/federated_lookup.py` (op_modelos): Find a model that a linked store registers, addressed as `alias:ModelName`.
- `api/model_registry/federated_registration.py` (op_modelos): Register, in a destination store, a model class that a linked store owns.
- `api/model_registry/inherit_model.py` (op_modelos): Inherit a model from the linked store that owns it, instead of keeping a copy of it.
- `api/stores/doc_ref.py` (op_almacen): Document references that may name a linked store: `deskops:task-x`, `deskops:TaskDoc/task-x`.
- `api/stores/doc_ref_status.py` (op_almacen): Whether a document reference resolves, as `doc_status` reports it.
- `api/stores/doc_status.py` (op_almacen): Does a document reference resolve? Answered from the stores' indexes, without importing it.
- `api/stores/link_store.py` (op_almacen): Link one store into another so its documents can be read through the linking store.
- `api/stores/linked_store.py` (op_almacen): A store link recorded in another store's index, as returned by `link_store`.
- `api/stores/migrate_hash_names.py` (op_almacen): `sldb stores migrate-hashes`: rewrite the persisted letter keys as their semantic names.
- `api/stores/migrate_layout.py` (op_almacen): `sldb stores migrate-layout`: move a store's cache from `.sldb/runtime/` to `.sldb_cache/`.
- `api/stores/store_links.py` (op_almacen): The links a store records, each with the state of its target computed when asked.
- `api/stores/tracked_documents.py` (op_almacen): Which of many references name a tracked document: `doc_status` asked once for all of them.
- `api/stores/unlink_store.py` (op_almacen): Remove a store link, or let `link_store(..., replace=True)` point it somewhere else.
- `store/catalog_reconcile.py` (op_almacen): Explicit discovery and reconciliation for a store catalog.
- `store/model_import_root.py` (op_modelos): The directory an owner's model imports from, read off the path the owner registers.
- `store/model_origin.py` (op_modelos): Where an inherited model comes from: the linked store that owns it.

### Lo que se hace con git encima (10)

- `api/documents/document_history.py` (op_documentos): `sldb docs history`: a document's past, read from git (docs/architecture/provenance.md §3).
- `api/documents/document_history_versions.py` (op_documentos): What one committed version of a document says: its provenance block, its hashes, its fields.
- `api/journal.py` (op_almacen): The write journal, retired on 2026-11-04: the store's past is read from git.
- `api/stores/conflict_sides.py` (op_almacen): Both sides of a file git left with conflict markers, and the by-name union of two lists.
- `api/stores/derived_recovery.py` (op_almacen): The data a derived index held before git broke it, read without trusting any hash in it.
- `api/stores/ensure_merge_driver.py` (op_almacen): The merge driver of a store inside a git repository: installed when the store is prepared
- `api/stores/gitignore_lines.py` (op_almacen): The lines sldb owns in the project's `.gitignore`: `.sldb_cache/` in, `.sldb/core/` and `.sldb/runtime/` out.
- `api/stores/gitignore_policy.py` (op_almacen): Whether the repository's ignore rules match the store's split.
- `api/stores/merge_driver.py` (op_almacen): `sldb stores merge-driver %O %A %B %P`: git's custom merge driver for a store's files.
- `api/stores/store_file_merge.py` (op_almacen): Merge two parsed versions of a store file: `store_index.yaml` (its lists by name) and

### NUEVO: Referencias del proyecto (50)

- `api/edges/referrer.py` (op_aristas): One incoming reference to a document or to a project graph node (GD22).
- `api/edges/referrer_frontmatter.py` (op_aristas): The frontmatter side of `referrers` (GD22): a mention on a frontmatter line of a document that is
- `api/edges/referrers.py` (op_aristas): `sldb.api.referrers(store, target)` (GD22): the incoming references of a document or of a
- `api/edges/rewrite_mentions.py` (op_aristas): Mentions of the target in prose (GD22): where the project graph of GD21 located them
- `api/edges/rewrite_plan.py` (op_aristas): The planning step of `rewrite_references` (GD22): the new payload of each referring document and
- `api/edges/rewrite_references.py` (op_aristas): `sldb.api.rewrite_references(store, target, replacement, *, transaction=None, dry_run=False,
- `api/edges/rewrite_report.py` (op_aristas): What `sldb.api.rewrite_references` did, or would do under `dry_run` (GD22).
- `api/edges/rewrite_values.py` (op_aristas): Declared field values that name the target (GD22): where the edge index places them
- `api/edges/project_graph/` (42 archivos, eje op_aristas): __init__, declaration, declared_file_targets, declared_target_nodes, document_declarations, document_edge_reader, document_metadata, document_node, document_nodes, document_surface, file_exclusions, file_node, file_nodes, file_rule, frontmatter_mapping, inverse_edges, line_mentions, mapping_declarations, mention_pattern, missing_project_target, missing_target_kind, node_lookup, node_provenance, path_text, project_edge, project_file_walk, project_graph, project_graph_config, project_graph_config_mapping, project_graph_extraction, project_graph_memo, project_nodes, project_store, project_texts, reference_field, section_mentions, source_edges, store_edges, store_project_graph, store_sources, store_unresolved, text_declarations. Leen el grafo de aristas declaradas de un proyecto (documentos y archivos como nodos, menciones, destinos que faltan).

### NUEVO: Diagnóstico del store (20)

- `api/stores/scan_cache.py` (op_almacen): Per-document results of the content scans of `stores check`, reused while nothing they
- `api/stores/scan_rewrite_loss.py` (op_almacen): Every tracked document a rewrite would lose content from, with what it would lose.
- `api/stores/scan_structural_noise.py` (op_almacen): Report the already-tracked documents whose headings their model never declares.
- `api/stores/store_check.py` (op_almacen): Store integrity check: the CLI's `sldb stores check` reached through sldb.api.
- `api/stores/store_check_summary.py` (op_almacen): The per-document projection of a store diagnosis for `check_store`: verdict by category and hash mismatches.
- `api/stores/store_findings.py` (op_almacen): A store diagnosis as findings: what is broken (error) apart from what moved (alert).
- `api/stores/store_surroundings.py` (op_almacen): What a store's surroundings say, as findings: its declaration, links, contents and ignores.
- `api/stores/unread_documents.py` (op_almacen): A tracked (or declared) document the store does not read (SEGURIDAD resto, after live_stale).
- `api/stores/unresolvable_documents.py` (op_almacen): Which indexed documents `docs show` cannot resolve, and why.
- `store/diagnostics.py` (op_almacen): (sin docstring) define diagnose_store
- `store/diagnostics_models/__init__.py` (op_almacen): (vacío)
- `store/diagnostics_models/diagnosis_note.py` (op_almacen): (sin docstring) define DiagnosisNote
- `store/diagnostics_models/document_diagnosis.py` (op_almacen): (sin docstring) define DocumentDiagnosis
- `store/diagnostics_models/document_verdicts.py` (op_almacen): What each document verdict means and what resolves it.
- `store/diagnostics_models/invalid_verdict.py` (op_almacen): The verdict of a tracked document its model rejects (inbox 3895e9f7, H1): `stores check` names
- `store/diagnostics_models/model_diagnosis.py` (op_almacen): (sin docstring) define ModelDiagnosis
- `store/diagnostics_models/store_diagnosis.py` (op_almacen): (sin docstring) define StoreDiagnosis
- `store/diagnostics_models/text_history.py` (op_almacen): Whether a document's indexed text is some version of the file git has seen.
- `store/diagnostics_models/unread_verdict.py` (op_almacen): The verdict of a tracked document that ``stores check`` does not read (SEGURIDAD live_stale,
- `store/diagnostics_models/verdict_notes.py` (op_almacen): The pieces of a document/model verdict: which fields moved, which note the hashes earn, and

### NUEVO: Declaración y montaje del store (14)

- `api/stores/apply_declaration.py` (op_almacen): Make a store match its declaration: links, models, predicates, then the tracked files.
- `api/stores/build_store.py` (op_almacen): `build_store`: the store made to match its declaration, in one report. Links, models,
- `api/stores/declaration_sync.py` (op_almacen): Keep `.sldb/store.yaml` true when a model is registered or a document is tracked or
- `api/stores/declare_store.py` (op_almacen): The declaration a store's current index implies: the starting `.sldb/store.yaml`.
- `api/stores/declared_files.py` (op_almacen): The `(model, path, name)` rows a declaration's `include` rules name: one per path.
- `api/stores/declared_includes.py` (op_almacen): The `include` rules that reproduce a store's current tracking, exactly.
- `api/stores/include_losers.py` (op_almacen): Untrack the rows a path's winning `include` rule beat, leaving the file alone.
- `api/stores/include_resolution.py` (op_almacen): One row per path when several `include` rules name it, or a `store/include-conflict`.
- `api/stores/merged_includes.py` (op_almacen): The `include` rules of a store that already declares them: kept as authored, then completed.
- `api/stores/scaffold_report.py` (op_almacen): What `scaffold_store` found or did, path by path (`docs/architecture/store-declaration.md`).
- `api/stores/scaffold_sources.py` (op_almacen): The bytes a seed's source stands for: `text` encoded, a `file` template read from the template
- `api/stores/scaffold_store.py` (op_almacen): `scaffold_store`: the folders and seed files a store declares, created or restored
- `api/stores/seed.py` (op_almacen): One `seeds` entry of a store declaration: a file the store scaffolds from a declared source
- `api/stores/store_declaration.py` (op_almacen): `.sldb/store.yaml`: what a store declares, the part of it that is source and lives in git.

### NUEVO: Escritura por lotes y transacciones (14)

- `api/documents/apply_batch.py` (op_documentos): Several document changes applied as one: prevalidated together, then written in one
- `api/documents/batch_edges.py` (op_documentos): The edge violations a batch would introduce, found before anything is written.
- `api/documents/batch_guards.py` (op_documentos): The guards a batch change can carry, checked against the document's current state before a write:
- `api/documents/batch_inverse.py` (op_documentos): The batch that undoes a batch (`BatchReport.inverse`): `before` notes, under the store lock and
- `api/documents/batch_prevalidate.py` (op_documentos): Prevalidation of a batch before any write (`apply_batch`): shape, model, payload round-trip (G4),
- `api/documents/batch_report.py` (op_documentos): What `apply_batch` applied, and the batch that undoes it.
- `api/documents/batch_simulation.py` (op_documentos): The edge index after a batch is applied in memory: its nodes, relations and relation types.
- `api/documents/nothing_to_undo.py` (op_documentos): The refusal of an undo with no such batch to undo.
- `api/documents/transaction.py` (op_documentos): Several document writes undone together: `transaction(store)` opens a `Transaction` whose
- `api/documents/transaction_ops.py` (op_documentos): The operations of a `Transaction`: each one the public function it names, with the files it
- `api/documents/transaction_paths.py` (op_documentos): Which files a document write may move, so a transaction snapshots them before the write;
- `api/documents/transaction_state.py` (op_documentos): The state one open transaction keeps over a store (`sldb.api.transaction`): how deeply it is
- `api/documents/undo_batches.py` (op_documentos): Undo the last applied batches of a store, from the write journal (`sldb.store.write_journal`):
- `api/documents/undo_report.py` (op_documentos): What `undo_batches` reverted.

### NUEVO: Contratos de modelo (editar el código del modelo) (31)

- `api/model_create/__init__.py` (op_modelos): Generate a model from a JSON declaration: `sldb.api.create_model` and its helpers.
- `api/model_create/create_model.py` (op_modelos): Generate a model from a JSON declaration, check it, write it and register it.
- `api/model_create/field_decl.py` (op_modelos): One field of a model declared in JSON: `{name, type, description, required?, default?,
- `api/model_create/model_check.py` (op_modelos): Whether a generated model module works before it is registered: it imports, its class is
- `api/model_create/model_declaration.py` (op_modelos): Validation of a model declaration: its fields and the field names its attributes cite.
- `api/model_create/model_generation.py` (op_modelos): Generate a model module from its declaration: base resolution, rendering, check, write.
- `api/model_create/model_module_lines.py` (op_modelos): The lines of a generated model module: header, class attributes and field declarations.
- `api/model_create/model_source.py` (op_modelos): The Python module of a model declared in JSON: a `StructuredNLDoc` written the way the
- `api/model_create/module_writing.py` (op_modelos): Write a generated model module under its package and refresh the import cache.
- `api/model_drafts/__init__.py` (op_modelos): Model contract drafts: edit fields, templates and metadata in a `.py.temp` sibling, validate, promote.
- `api/model_drafts/backfill.py` (op_modelos): Check every document under a draft and plan the backfill of new fields.
- `api/model_drafts/composition_contract.py` (op_modelos): Check that a model's compositions name known source fields and have render markers.
- `api/model_drafts/draft_checks.py` (op_modelos): The registry facts a draft validation needs; document checks live in `backfill`.
- `api/model_drafts/draft_contract.py` (op_modelos): Check that a model's template only references fields the model declares.
- `api/model_drafts/draft_document_check.py` (op_modelos): The result of checking one tracked document against a model draft.
- `api/model_drafts/draft_loading.py` (op_modelos): Load a model class from a draft source file without replacing the imported module.
- `api/model_drafts/draft_restore.py` (op_modelos): Snapshot the files a promotion rewrites, and put them back if the promotion fails.
- `api/model_drafts/draft_validation.py` (op_modelos): Validate a model's draft contract against its tracked documents, and promote it.
- `api/model_drafts/draft_validation_report.py` (op_modelos): Outcome of validating (and possibly promoting) a model draft.
- `api/model_drafts/field_blocks.py` (op_modelos): Insert or remove one field declaration in a model class's source text.
- `api/model_drafts/field_drafts.py` (op_modelos): Add or remove a field in a model's draft contract.
- `api/model_drafts/metadata_composition_sync.py` (op_modelos): Keep a draft's template in step with the compositions an edit adds or removes.
- `api/model_drafts/metadata_drafts.py` (op_modelos): Edit class-level metadata (__containment__, __references__, __compositions__, __semantics__, __authority__) in a model d
- `api/model_drafts/metadata_literals.py` (op_modelos): Read, replace or insert class-level metadata assignments in a model's source text.
- `api/model_drafts/model_draft.py` (op_modelos): A pending edit of a model's contract, as returned by the draft-editing operations.
- `api/model_drafts/model_source.py` (op_modelos): Where a registered model class is defined, as returned by `locate_model_source`.
- `api/model_drafts/source_editing.py` (op_modelos): Edit Python source text by AST node positions, keeping every other byte intact.
- `api/model_drafts/source_location.py` (op_modelos): Locate the source file that defines a registered model, following re-export modules.
- `api/model_drafts/template_drafts.py` (op_modelos): Replace the Markdown template of a model's draft contract.
- `api/model_drafts/template_literals.py` (op_modelos): Read or replace the `__template__` literal of a model class in its source text.
- `api/model_drafts/template_sections.py` (op_modelos): The `## Title` template section `add_model_field` appends (and `remove_model_field` drops).

## Partir

Archivos que hacen dos cosas de módulos distintos. El destino de la tabla es el de la parte mayor.

**Con su propia llamada a git (7 archivos).** Ninguno usa un ayudante común: cada uno hace su
`subprocess.run(["git", ...])`. En total son 10 archivos del bloque con esa llamada (3 ya son
puramente de la interfaz: `relocate_file`, `branch_stores`, `merge_driver_install`). El resto mezcla
la llamada con lógica propia:

| Archivo | Parte A (destino de la tabla) | Parte B: la llamada a git |
|---|---|---|
| `api/documents/move_path_files.py` | Operaciones: qué archivos toca un movimiento | Interfaz con git: `git ls-files` |
| `api/documents/document_history.py` | git encima: historia de un documento | Interfaz con git: `git log --follow` y `git show` |
| `api/stores/ensure_merge_driver.py` | git encima: instalar el driver | Interfaz con git: `rev-parse`, `config --get` |
| `api/stores/derived_recovery.py` | git encima: recuperar un índice roto | Interfaz con git: `git show HEAD:` |
| `api/stores/gitignore_policy.py` | git encima: política de `.gitignore` | Interfaz con git: `rev-parse`, `check-ignore` |
| `store/diagnostics_models/text_history.py` | Diagnóstico: ¿este texto lo vio git? | Interfaz con git |
| `store/package_version.py` | Política: versión para el sello de procedencia | Interfaz con git: `git describe` |

(`api/stores/apply_findings.py` también usa `subprocess`, pero para correr el comando de la política,
no git.)

**Otros.**

| Archivo | Parte A | Parte B |
|---|---|---|
| `api/graph/analyze.py` | Análisis del grafo: caminos, ciclos, componentes, centralidad | Similitud: `graph_similar` (una función de diez) |
| `api/stores/open_store.py` | Datos: resolver el store y empezar una operación | Varios stores y migración: `migrate_store_layout` y `add_owner_import_roots` (modelos heredados) |
| `api/segments/segment_enrichment.py` | Documentos con forma: `table_data` de un segmento | Notaciones y vistas: la `projection` de un segmento de vista o diagrama |
| `api/stores/store_declaration.py` | Declaración: el modelo de `store.yaml` | Datos: `declared_store` ubica el store sin índice (menor) |
| `runtime/validation.py` (fuera del bloque) | Documentos con forma: validar un modelo contra su texto | Árboles: `extract_payload(template, md)` y `render_markdown(template, data)` no necesitan un modelo (ver "Las tres funciones") |

Total a partir dentro del bloque: **11 archivos** (los 7 de git, `analyze`, `open_store`,
`segment_enrichment` y `store_declaration`). `runtime/validation.py` también se parte, pero está fuera del bloque.

## Sin módulo

Ningún archivo quedó sin casa en absoluto: todos caben en algún módulo de `modulos.md` si se fuerza
el criterio. Pero 129 archivos caben solo a medias. Hacen algo coherente que ningún módulo nombra.
Los agrupé por parecido. Cada grupo tiene 14 archivos o más, así que pasa el umbral de 4.

1. **Referencias del proyecto (50 archivos, eje op_aristas).** Lee, de los documentos y de los
   archivos de un proyecto, qué se declara que apunta a qué: frontmatter, bloques YAML, menciones en
   líneas y secciones. Hace de eso un grafo con nodos de documento y de archivo, marca destinos que
   no existen, calcula quién referencia a quién (`referrers`) y reescribe las referencias cuando algo
   se mueve (`rewrite_references`). Hoy `project_graph/` son 42 archivos y los otros 8 son
   `referrer*` y `rewrite_*`. Por qué no es Enlaces y transclusión: eso son los enlaces dentro de un
   texto; esto es el grafo declarado de todo el proyecto, con archivos de código como nodos. Por qué
   no es Análisis del grafo: no analiza, construye el grafo. Decisión abierta: puede ser una parte de
   Enlaces si se define Enlaces como "toda referencia".
2. **Contratos de modelo: editar el código del modelo (31 archivos, eje op_modelos).**
   `model_create/` (9) genera un módulo Python de modelo desde una declaración JSON. `model_drafts/`
   (22) edita campos, plantilla y metadatos de la clase en un `.py.temp` junto al original, lo
   valida contra los documentos, rellena campos nuevos (`backfill`) y lo promueve. Casi la mitad es
   edición de texto Python por posiciones del AST (`source_editing`, `field_blocks`,
   `metadata_literals`, `template_literals`). Por qué no es Documentos con forma: eso define cómo es
   un documento; esto reescribe el código de la clase que lo define. Por qué no es Código a
   documentos: ese módulo lee código, este lo escribe.
3. **Diagnóstico del store (20 archivos, eje op_almacen).** `stores check`: la diagnosis de cada
   documento y modelo (`store/diagnostics*`, 11 archivos), el reporte y los hallazgos (`store_check`,
   `store_findings`, `store_surroundings`), los escaneos de pérdida y de ruido estructural con su
   caché, y los documentos sin leer o sin resolver. Compone Datos, Anclaje (hashes) y Reglas, y no es
   ninguno.
4. **Declaración y montaje del store (14 archivos, eje op_almacen).** `.sldb/store.yaml`: qué
   declara un store (links, modelos, includes, seeds), cómo se deduce de un índice existente
   (`declare_store`), cómo se resuelven los `include` en conflicto y cómo se monta el store para que
   coincida (`build_store`, `apply_declaration`, `scaffold_store`). Es lo "declarativo" del store.
   Se acerca a Declaraciones evaluadas, pero esa es de recetas evaluadas (kimun); esta es la
   declaración del propio store. Los grupos 3 y 4 juntos (34 archivos) podrían ser un solo módulo
   "Ciclo de vida del store" si se les suman los archivos de Datos que crean y reconstruyen índices.
5. **Escritura por lotes y transacciones (14 archivos, eje op_documentos).** `apply_batch` y sus
   cinco apoyos (`batch_*`: prevalidar, guardas, simular el índice, calcular el inverso, reportar),
   `transaction*` (cinco archivos: abrir, deshacer en conjunto, qué archivos se tocan) y `undo_batches`.
   Una escritura atómica y reversible sobre varios documentos. Decisión abierta: podría ser el lado
   de escritura de Datos (en Datomic la transacción es parte del motor). No lo asigné a Datos porque
   cada pieza llama a validación de modelos, aristas y reglas, que son librerías.

## Las tres funciones de la deuda de imports

**`api.stores.open_store` (48 usos) pertenece a Datos (kernel).** Resuelve dónde vive el store,
migra el layout si hace falta y arranca una operación nueva sobre sus cachés. Solo importa de
`store.*` y de `store_discovery`; no usa modelos, reglas ni aristas. Es la puerta de entrada de
todo lo demás, y por eso es deuda: está dentro de `api`, un anillo por encima de quienes la llaman
(`store/`, `models/` y otras capas bajas la necesitan). Debe moverse al módulo Datos junto con
`store_location` y `store_discovery`. Sobra una parte: la migración de layout y las raíces de
importación de modelos heredados no son de Datos (Varios stores y migración); `open_store` tendría
que llamarlas por un gancho y no importarlas.

**`api.stores.store_location` (12 usos) pertenece a Datos (kernel).** `StoreLocation` es un modelo de
dos campos (`store_path`, `project_root`) que devuelve `open_store`. Es el tipo del resultado de
Datos y viaja con la función que lo produce. La deuda es la misma: lo importan 12 archivos de
operación (`batch_*`, `transaction_state`, `move_path_*`, `referrers`...) y está un anillo
más arriba.

**`runtime.validation` (18 usos) se reparte entre dos módulos.** El archivo tiene dos mitades:
(a) `extract_payload(template, markdown)` y `render_markdown(template, data)` trabajan solo con una
plantilla y un texto, sin tipos de modelo. Son el ida y vuelta texto-estructura y pertenecen a
Árboles (kernel). (b) `Validator`, `extract_model_data`, `validate_model_*_roundtrip` y
`render_model_markdown` toman la clase del modelo (`StructuredNLDoc`). Pertenecen a Documentos con
forma (librería). Los 18 usos están en `api/` (`create_document`, `batch_prevalidate`, `track_document_file`,
`replace_text`, `payload_save_steps`, `draft_contract`, `view_source`, `scaffold_sources`...). Además
la importan otros 9 archivos: dos de capas bajas (`store/runtime_codec.py`, `models/structured_doc.py`),
cinco de `cli/` y dos de `selfdoc/`. O sea que el kernel (Datos) necesita la mitad (a) y hoy la toma de
un anillo superior. Con el reparto, el kernel solo importaría la mitad de Árboles, y los 18 usuarios
de `api/` usarían la mitad (b) (librería) o la (a) (kernel) según lo que llamen.

## Archivos muertos

Búsqueda por imports reales (con `ast`) y por nombre de símbolo en `src/` y `tests/`, excluyendo el
propio archivo. Cuidado: casi todos estos símbolos están reexportados en `sldb/api/__init__.py`,
o sea que son superficie pública de la librería aunque nadie los use dentro del repo. Los marco
como muertos para el repo, no como borrables sin preguntar.

Sin ningún usuario en `src/` ni en `tests/` (solo reexportados), 3 archivos:

- `api/edges/edges_blocked.py`: solo `src/sldb/api/__init__.py` lo importa. Se nombra en docstrings.
- `api/graph/traverse.py`: `targets`, `sources`, `roots`, `children`, `parent`, `descendants`,
  `neighbors_via`, `exists`. Solo lo importa `api/graph/__init__.py`. La lógica real vive en
  `store/graph/traversal.py`.
- `api/schema/field_description.py`: shim ("Moved to `sldb.models.field_schema.description`"), sin
  símbolos propios.

Con usuarios solo en `tests/`, 8 archivos (vivos solo para su prueba):

- `api/documents/payload_diff.py`: lo importa una prueba (`test_model_lifecycle`); `field_label` no lo usa nadie.
- `api/edges/apply_effects.py`: `tests/api/test_edge_effects.py`.
- `api/model_registry/template_anchors.py`: `tests/test_literal_paragraph_anchor.py`.
- `api/schema/describe_field.py`: `describe_model_fields` solo en una prueba; `schema_snapshot` no lo usa nadie.
- `api/stores/read_store.py`: `tests/api/test_api_stores.py`.
- `api/tags/tag_folder.py`: `tests/api/test_tags.py`.
- `api/code/code_facts.py` y `api/code/requested_files.py`: `tests/selfdoc/test_treesitter_symbols.py`.

No cuento como muertos: `api/journal.py` (retirado, pero `cli/commands/journal.py` lo importa),
`api/documents/undo_batches.py`, `api/anchors/resolve_pointers.py` y `api/stores/store_fingerprint.py`
(los usa `mcp/` por `api.<nombre>`), ni `api/records/ast_target.py` (lo reexporta `cli/graph_ops`).

Total: **3 muertos del todo y 8 solo para pruebas**. La búsqueda no revisó lo que se invoca por
nombre desde datos (YAML, TOML, docs), solo código Python.

## Límites de este análisis

- Cada destino sale de lo que el archivo hace según su docstring, nombres e imports, no de leer
  los cuerpos completos. Los archivos de `api/records/` y de `store/diagnostics*` no tienen
  docstring; ahí decidí por nombres e imports.
- La parte de la interfaz con git del kernel no existe como archivo: son 10 llamadas sueltas, cada una con su `subprocess`.
