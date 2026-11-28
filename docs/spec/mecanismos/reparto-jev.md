# Reparto del bloque operación, clasificado con Jev

Fecha: 2026-11-27. Estado: **resultado de una clasificación automática, sin revisar**. No se
movió código.

Qué es: cada uno de los 355 archivos de los siete ejes del bloque operación (`op_documentos`,
`op_modelos`, `op_aristas`, `op_almacen`, `anclaje`, `reglas`, `vistas_compuestas`) se le mostró
a Jev, un modelo de decisiones de TypeSafe, con su ruta, su docstring, sus nombres públicos y
sus imports. Se le hicieron tres preguntas por archivo: a cuál de veinte módulos pertenece, si
de verdad calza en alguno, y si hace dos trabajos de módulos distintos. Devuelve probabilidades,
no texto. Los datos completos, con las tres mejores opciones por archivo, están en
`reparto-jev.json`.

Los veinte destinos son los módulos de `modulos.md`, con tres agregados para ver si aparecían:
"grafo de proyecto", "administración del store", y "modelos" y "relaciones" separados de
"documentos".

"Seguro" quiere decir confianza de 0,7 o más en el módulo y 0,6 o más en que calza.

## Resumen

| Módulo destino | Archivos | Líneas | Seguros | Confianza media |
|---|---|---|---|---|
| Documentos con modelo | 59 | 3386 | 36 | 0.76 |
| Modelos | 46 | 2414 | 38 | 0.85 |
| Administración del store | 43 | 2838 | 25 | 0.73 |
| Grafo de proyecto | 43 | 2118 | 31 | 0.82 |
| Kernel: datos | 34 | 1807 | 13 | 0.63 |
| Reglas, estados y política | 23 | 1297 | 15 | 0.75 |
| Relaciones declaradas | 15 | 794 | 8 | 0.69 |
| Kernel: árboles | 14 | 598 | 6 | 0.68 |
| Varios stores y migración | 13 | 770 | 10 | 0.76 |
| Lo que se hace con git | 11 | 606 | 9 | 0.89 |
| Cara | 10 | 310 | 2 | 0.57 |
| Kernel: anclaje | 9 | 567 | 8 | 0.85 |
| Notaciones y vistas | 9 | 500 | 4 | 0.66 |
| Semántica | 7 | 338 | 6 | 0.85 |
| Enlaces en el texto | 5 | 183 | 0 | 0.37 |
| Fachada | 5 | 121 | 2 | 0.75 |
| Kernel: consultas y reglas | 3 | 180 | 2 | 0.69 |
| Análisis del grafo | 3 | 230 | 2 | 0.81 |
| Código a documentos | 2 | 85 | 0 | 0.58 |
| Kernel: interfaz con git | 1 | 71 | 0 | 0.56 |

De 355 archivos, 217 quedan seguros y 69 dudosos. Ningún archivo salió marcado como mezcla de dos
trabajos (la probabilidad más alta fue 0.45); eso dice que los archivos son chicos y de un solo
propósito, no que estén bien ubicados.

## De dónde viene cada módulo

| Eje de hoy | A dónde van sus archivos |
|---|---|
| `anclaje` | Kernel: anclaje 7, Código a documentos 2, Semántica 1 |
| `op_almacen` | Administración del store 38, Kernel: datos 17, Documentos con modelo 10, Lo que se hace con git 10, Varios stores y migración 7, Reglas, estados y política 4, Fachada 2, Enlaces en el texto 1, Grafo de proyecto 1, Kernel: árboles 1, Kernel: consultas y reglas 1, Cara 1, Relaciones declaradas 1, Semántica 1, Kernel: anclaje 1, Kernel: interfaz con git 1 |
| `op_aristas` | Grafo de proyecto 42, Relaciones declaradas 13, Kernel: datos 7, Administración del store 4, Análisis del grafo 2, Fachada 2, Reglas, estados y política 1, Cara 1, Varios stores y migración 1 |
| `op_documentos` | Documentos con modelo 48, Kernel: árboles 12, Kernel: datos 8, Cara 7, Enlaces en el texto 4, Kernel: consultas y reglas 2, Relaciones declaradas 1, Kernel: anclaje 1, Lo que se hace con git 1, Reglas, estados y política 1, Notaciones y vistas 1, Administración del store 1 |
| `op_modelos` | Modelos 46, Varios stores y migración 4, Documentos con modelo 1, Kernel: árboles 1, Kernel: datos 1, Fachada 1, Cara 1 |
| `reglas` | Reglas, estados y política 15, Semántica 5, Kernel: datos 1 |
| `vistas_compuestas` | Notaciones y vistas 8, Reglas, estados y política 2, Análisis del grafo 1, Varios stores y migración 1 |

## Lo que muestra

- **Dos módulos nuevos aparecen con claridad.** "Grafo de proyecto" recibe 43 archivos con
  confianza alta: es todo `api/edges/project_graph`, que arma un grafo de un repositorio entero
  desde sus archivos. Y "administración del store" recibe 43: iniciar, declarar, construir,
  revisar, diagnosticar y exportar un store. Ninguno de los dos estaba en la lista original.
- **"Operaciones" no existe como módulo.** Se reparte en documentos (59), modelos (46) y
  relaciones (15), como anticipó JP.
- **Abrir y ubicar un store son del kernel de datos.** `api/stores/open_store.py` y
  `store_location.py` salen en "Kernel: datos" con confianza 0,72 y 0,89. Son las funciones que
  sostienen 60 de los 138 imports de la deuda de anillos: están en el anillo 2 y las usa el
  anillo 0.
- **34 archivos del bloque operación son en realidad kernel de datos**, 14 son árboles y 9 son
  anclaje. Están en la capa de composición y son piezas del centro.
- **Una carpeta no calza en nada: `api/records`** (18 archivos, ajuste medio 0,51). Lee el store
  "por registros" y Jev la reparte entre ocho módulos distintos. Es candidata a módulo propio o
  a desaparecer. Le siguen `store/diagnostics_models` y `api/segments`.

## Límites

- Jev vio el docstring, los nombres públicos y los imports, no el cuerpo de las funciones.
- Las descripciones de los veinte módulos las escribió el agente; otra redacción daría otro
  reparto en los casos dudosos.
- No se evaluó contra una clasificación hecha a mano. Queda por cruzar con el reparto que está
  haciendo un agente leyendo los archivos (`reparto-operacion.md`): donde los dos coincidan, se
  puede confiar; donde no, hay que mirar.

## Dudosos

Confianza menor a 0,5 o ajuste menor a 0,4. La segunda columna es lo que eligió; la tercera, su
segunda opción.

| Archivo | Eligió | Segunda opción | Confianza | Ajuste |
|---|---|---|---|---|
| `api/segments/segment_nodes.py` | Cara | Código a documentos | 0.21 | 0.21 |
| `api/actor.py` | Cara | Documentos con modelo | 0.47 | 0.26 |
| `api/records/utils.py` | Documentos con modelo | Kernel: datos | 0.14 | 0.29 |
| `api/records/runtime_doc_proxy.py` | Documentos con modelo | Fachada | 0.22 | 0.34 |
| `store/package_version.py` | Kernel: interfaz con git | Cara | 0.56 | 0.34 |
| `api/records/matches.py` | Kernel: datos | Fachada | 0.28 | 0.41 |
| `api/journal.py` | Fachada | Kernel: datos | 0.36 | 0.42 |
| `api/records/flatten.py` | Kernel: datos | Cara | 0.33 | 0.42 |
| `api/documents/data_values.py` | Cara | Documentos con modelo | 0.31 | 0.43 |
| `api/segments/segment_enrichment.py` | Notaciones y vistas | Kernel: árboles | 0.26 | 0.43 |
| `api/views/view_groups.py` | Notaciones y vistas | Cara | 0.45 | 0.44 |
| `store/diagnostics_models/document_diagnosis.py` | Administración del store | Documentos con modelo | 0.34 | 0.45 |
| `api/records/iter_records_helpers.py` | Documentos con modelo | Kernel: datos | 0.22 | 0.46 |
| `api/records/iter_records.py` | Documentos con modelo | Kernel: datos | 0.46 | 0.47 |
| `api/records/build_ir.py` | Grafo de proyecto | Administración del store | 0.18 | 0.49 |
| `api/documents/document_payload.py` | Documentos con modelo | Cara | 0.39 | 0.52 |
| `api/records/search_record.py` | Kernel: datos | Kernel: consultas y reglas | 0.46 | 0.53 |
| `api/documents/runtime_documents.py` | Documentos con modelo | Fachada | 0.49 | 0.54 |
| `api/records/build_ast.py` | Administración del store | Kernel: datos | 0.45 | 0.55 |
| `api/records/iter_records_docs.py` | Documentos con modelo | Administración del store | 0.22 | 0.55 |
| `api/records/map_fields.py` | Documentos con modelo | Kernel: árboles | 0.31 | 0.55 |
| `api/stores/merged_includes.py` | Administración del store | Reglas, estados y política | 0.45 | 0.55 |
| `api/records/ast_target.py` | Enlaces en el texto | Documentos con modelo | 0.21 | 0.56 |
| `api/stores/ambiguous_document.py` | Varios stores y migración | Documentos con modelo | 0.29 | 0.57 |
| `api/stores/doc_ref_status.py` | Relaciones declaradas | Enlaces en el texto | 0.43 | 0.57 |
| `api/documents/structural_noise_report.py` | Documentos con modelo | Modelos | 0.19 | 0.59 |
| `api/records/resolve.py` | Documentos con modelo | Fachada | 0.40 | 0.59 |
| `store/diagnostics_models/diagnosis_note.py` | Administración del store | Modelos | 0.35 | 0.59 |
| `api/edges/edge_effects.py` | Relaciones declaradas | Reglas, estados y política | 0.42 | 0.60 |
| `api/segments/source_ref.py` | Enlaces en el texto | Kernel: árboles | 0.24 | 0.60 |
| `api/documents/select_documents.py` | Kernel: consultas y reglas | Fachada | 0.40 | 0.61 |
| `api/stores/tracked_documents.py` | Kernel: datos | Documentos con modelo | 0.28 | 0.61 |
| `api/documents/extract_payload.py` | Documentos con modelo | Kernel: árboles | 0.42 | 0.63 |
| `api/records/section_record.py` | Kernel: datos | Kernel: árboles | 0.39 | 0.63 |
| `api/stores/declared_files.py` | Reglas, estados y política | Administración del store | 0.37 | 0.63 |
| `api/stores/scan_rewrite_loss.py` | Documentos con modelo | Administración del store | 0.26 | 0.63 |
| `api/edges/builtin_relation_writes.py` | Relaciones declaradas | Administración del store | 0.47 | 0.64 |
| `api/model_registry/template_anchors.py` | Modelos | Documentos con modelo | 0.38 | 0.64 |
| `api/segments/field_segment.py` | Kernel: árboles | Notaciones y vistas | 0.27 | 0.64 |
| `api/graph/snapshot.py` | Administración del store | Fachada | 0.44 | 0.65 |
| `api/schema/store_schema.py` | Cara | Modelos | 0.45 | 0.65 |
| `api/views/view_revision.py` | Notaciones y vistas | Kernel: datos | 0.41 | 0.65 |
| `api/model_drafts/draft_restore.py` | Modelos | Kernel: datos | 0.31 | 0.66 |
| `api/segments/composition_spec.py` | Enlaces en el texto | Modelos | 0.34 | 0.66 |
| `api/views/view_nodes.py` | Varios stores y migración | Análisis del grafo | 0.31 | 0.66 |
| `api/stores/doc_status.py` | Kernel: datos | Varios stores y migración | 0.25 | 0.67 |
| `api/documents/relocate_file.py` | Documentos con modelo | Kernel: interfaz con git | 0.39 | 0.68 |
| `api/records/extract.py` | Kernel: árboles | Código a documentos | 0.44 | 0.68 |
| `api/stores/declared_includes.py` | Administración del store | Kernel: datos | 0.48 | 0.68 |
| `api/stores/include_resolution.py` | Administración del store | Reglas, estados y política | 0.40 | 0.69 |
| `api/model_registry/model_document_summary.py` | Modelos | Documentos con modelo | 0.48 | 0.70 |
| `api/model_registry/model_index_writes.py` | Modelos | Kernel: datos | 0.48 | 0.70 |
| `store/diagnostics_models/verdict_notes.py` | Kernel: anclaje | Administración del store | 0.42 | 0.71 |
| `api/documents/move_path_links.py` | Enlaces en el texto | Relaciones declaradas | 0.40 | 0.72 |
| `api/edges/project_graph/project_store.py` | Kernel: datos | Grafo de proyecto | 0.48 | 0.72 |
| `store/field_set_drift.py` | Kernel: datos | Documentos con modelo | 0.46 | 0.72 |
| `api/segments/build_document_segments.py` | Kernel: árboles | Notaciones y vistas | 0.49 | 0.73 |
| `api/stores/include_losers.py` | Kernel: datos | Administración del store | 0.41 | 0.73 |
| `api/edges/relation_models.py` | Varios stores y migración | Relaciones declaradas | 0.38 | 0.74 |
| `store/diagnostics_models/invalid_verdict.py` | Documentos con modelo | Administración del store | 0.48 | 0.75 |
| `api/edges/project_graph/reference_field.py` | Grafo de proyecto | Modelos | 0.48 | 0.76 |
| `api/model_registry/registration_query.py` | Modelos | Varios stores y migración | 0.49 | 0.76 |
| `api/stores/indexed_documents.py` | Kernel: datos | Varios stores y migración | 0.35 | 0.77 |
| `api/edges/check_edges.py` | Relaciones declaradas | Administración del store | 0.49 | 0.78 |
| `api/documents/on_write_gate.py` | Reglas, estados y política | Reglas, estados y política | 0.45 | 0.80 |
| `api/edges/project_graph/store_edges.py` | Grafo de proyecto | Relaciones declaradas | 0.49 | 0.81 |
| `api/edges/project_graph/project_edge.py` | Grafo de proyecto | Relaciones declaradas | 0.39 | 0.82 |
| `api/edges/relations_init_report.py` | Relaciones declaradas | Administración del store | 0.47 | 0.82 |
| `api/edges/edge_check_report.py` | Administración del store | Kernel: datos | 0.43 | 0.84 |

## Reparto completo

### Documentos con modelo (59)

`api/documents/apply_batch.py`, `api/documents/batch_guards.py`, `api/documents/batch_inverse.py`, `api/documents/batch_prevalidate.py`, `api/documents/batch_report.py`, `api/documents/content_hash.py`, `api/documents/create_document.py`, `api/documents/delete_document.py`, `api/documents/document_history_versions.py`, `api/documents/document_payload.py`, `api/documents/document_reference.py`, `api/documents/extract_payload.py`, `api/documents/frontmatter_keys.py`, `api/documents/invalid_document.py`, `api/documents/lossy_overwrite.py`, `api/documents/move_document.py`, `api/documents/move_path.py`, `api/documents/move_path_apply.py`, `api/documents/move_path_fields.py`, `api/documents/move_path_files.py`, `api/documents/move_path_plan.py`, `api/documents/move_path_remap.py`, `api/documents/move_path_report.py`, `api/documents/move_path_resolve.py`, `api/documents/nothing_to_undo.py`, `api/documents/payload_diff.py`, `api/documents/payload_path_reading.py`, `api/documents/payload_path_writing.py`, `api/documents/payload_save.py`, `api/documents/payload_save_steps.py`, `api/documents/provenance_stamp.py`, `api/documents/refuse_structural_noise.py`, `api/documents/relocate_file.py`, `api/documents/replace_text.py`, `api/documents/rewrite_loss.py`, `api/documents/runtime_documents.py`, `api/documents/structural_noise.py`, `api/documents/structural_noise_report.py`, `api/documents/track_document_file.py`, `api/documents/transaction.py`, `api/documents/transaction_ops.py`, `api/documents/transaction_paths.py`, `api/documents/transaction_state.py`, `api/documents/undo_batches.py`, `api/documents/undo_report.py`, `api/documents/untrack_document.py`, `api/model_drafts/draft_document_check.py`, `api/records/fields.py`, `api/records/iter_records.py`, `api/records/iter_records_docs.py`, `api/records/iter_records_helpers.py`, `api/records/map_fields.py`, `api/records/resolve.py`, `api/records/runtime_doc_proxy.py`, `api/records/utils.py`, `api/segments/field_ref_resolver.py`, `api/segments/payload_values.py`, `api/stores/scan_rewrite_loss.py`, `store/diagnostics_models/invalid_verdict.py`

### Modelos (46)

`api/model_create/create_model.py`, `api/model_create/field_decl.py`, `api/model_create/model_check.py`, `api/model_create/model_declaration.py`, `api/model_create/model_generation.py`, `api/model_create/model_module_lines.py`, `api/model_create/model_source.py`, `api/model_create/module_writing.py`, `api/model_drafts/backfill.py`, `api/model_drafts/composition_contract.py`, `api/model_drafts/draft_checks.py`, `api/model_drafts/draft_contract.py`, `api/model_drafts/draft_loading.py`, `api/model_drafts/draft_restore.py`, `api/model_drafts/draft_validation.py`, `api/model_drafts/draft_validation_report.py`, `api/model_drafts/field_blocks.py`, `api/model_drafts/field_drafts.py`, `api/model_drafts/metadata_composition_sync.py`, `api/model_drafts/metadata_drafts.py`, `api/model_drafts/metadata_literals.py`, `api/model_drafts/model_draft.py`, `api/model_drafts/model_source.py`, `api/model_drafts/source_location.py`, `api/model_drafts/template_drafts.py`, `api/model_drafts/template_literals.py`, `api/model_drafts/template_sections.py`, `api/model_registry/add_model.py`, `api/model_registry/describe_model.py`, `api/model_registry/load_registered_model.py`, `api/model_registry/model_class_attrs.py`, `api/model_registry/model_description.py`, `api/model_registry/model_document_summary.py`, `api/model_registry/model_field_summary.py`, `api/model_registry/model_index_writes.py`, `api/model_registry/model_lineage.py`, `api/model_registry/model_reference.py`, `api/model_registry/model_registration.py`, `api/model_registry/registered_model.py`, `api/model_registry/registration_query.py`, `api/model_registry/reindex_model.py`, `api/model_registry/remove_model.py`, `api/model_registry/template_anchors.py`, `api/schema/describe_field.py`, `api/schema/unavailable_model.py`, `store/model_import_root.py`

### Administración del store (43)

`api/edges/edge_check_report.py`, `api/edges/init_relations.py`, `api/edges/rebuild_edges.py`, `api/graph/snapshot.py`, `api/records/build_ast.py`, `api/stores/apply_declaration.py`, `api/stores/apply_findings.py`, `api/stores/build_store.py`, `api/stores/declaration_sync.py`, `api/stores/declare_store.py`, `api/stores/declared_includes.py`, `api/stores/include_resolution.py`, `api/stores/index_commit.py`, `api/stores/index_refresh.py`, `api/stores/init_store.py`, `api/stores/merged_includes.py`, `api/stores/rebuild_index.py`, `api/stores/scaffold_report.py`, `api/stores/scaffold_sources.py`, `api/stores/scaffold_store.py`, `api/stores/scan_cache.py`, `api/stores/scan_structural_noise.py`, `api/stores/seed.py`, `api/stores/store_check.py`, `api/stores/store_check_summary.py`, `api/stores/store_declaration.py`, `api/stores/store_findings.py`, `api/stores/store_skeleton.py`, `api/stores/store_surroundings.py`, `api/stores/store_update_report.py`, `api/stores/unread_documents.py`, `api/stores/unresolvable_documents.py`, `api/stores/update_store_indexes.py`, `store/catalog_reconcile.py`, `store/diagnostics.py`, `store/diagnostics_models/diagnosis_note.py`, `store/diagnostics_models/document_diagnosis.py`, `store/diagnostics_models/document_verdicts.py`, `store/diagnostics_models/model_diagnosis.py`, `store/diagnostics_models/store_diagnosis.py`, `store/diagnostics_models/unread_verdict.py`, `store/export.py`, `store/section_rebuild.py`

### Grafo de proyecto (43)

`api/edges/project_graph/declaration.py`, `api/edges/project_graph/declared_file_targets.py`, `api/edges/project_graph/declared_target_nodes.py`, `api/edges/project_graph/document_declarations.py`, `api/edges/project_graph/document_edge_reader.py`, `api/edges/project_graph/document_metadata.py`, `api/edges/project_graph/document_node.py`, `api/edges/project_graph/document_nodes.py`, `api/edges/project_graph/document_surface.py`, `api/edges/project_graph/file_exclusions.py`, `api/edges/project_graph/file_node.py`, `api/edges/project_graph/file_nodes.py`, `api/edges/project_graph/file_rule.py`, `api/edges/project_graph/frontmatter_mapping.py`, `api/edges/project_graph/inverse_edges.py`, `api/edges/project_graph/line_mentions.py`, `api/edges/project_graph/mapping_declarations.py`, `api/edges/project_graph/mention_pattern.py`, `api/edges/project_graph/missing_project_target.py`, `api/edges/project_graph/missing_target_kind.py`, `api/edges/project_graph/node_lookup.py`, `api/edges/project_graph/node_provenance.py`, `api/edges/project_graph/path_text.py`, `api/edges/project_graph/project_edge.py`, `api/edges/project_graph/project_file_walk.py`, `api/edges/project_graph/project_graph.py`, `api/edges/project_graph/project_graph_config.py`, `api/edges/project_graph/project_graph_config_mapping.py`, `api/edges/project_graph/project_graph_extraction.py`, `api/edges/project_graph/project_graph_memo.py`, `api/edges/project_graph/project_nodes.py`, `api/edges/project_graph/project_texts.py`, `api/edges/project_graph/reference_field.py`, `api/edges/project_graph/section_mentions.py`, `api/edges/project_graph/source_edges.py`, `api/edges/project_graph/store_edges.py`, `api/edges/project_graph/store_project_graph.py`, `api/edges/project_graph/store_sources.py`, `api/edges/project_graph/store_unresolved.py`, `api/edges/project_graph/text_declarations.py`, `api/edges/referrer_frontmatter.py`, `api/edges/rewrite_mentions.py`, `api/records/build_ir.py`

### Kernel: datos (34)

`api/documents/batch_simulation.py`, `api/documents/doc_hashes.py`, `api/documents/document_lookup.py`, `api/edges/edge_evidence.py`, `api/edges/edge_reading.py`, `api/edges/project_graph/project_store.py`, `api/model_registry/model_files.py`, `api/records/flatten.py`, `api/records/matches.py`, `api/records/search_record.py`, `api/records/section_record.py`, `api/rules/rule_cache.py`, `api/stores/doc_status.py`, `api/stores/document_field_hashes.py`, `api/stores/include_losers.py`, `api/stores/indexed_documents.py`, `api/stores/open_store.py`, `api/stores/read_store.py`, `api/stores/resolve_indexed_document.py`, `api/stores/store_discovery.py`, `api/stores/store_fingerprint.py`, `api/stores/store_location.py`, `api/stores/tracked_documents.py`, `store/documents_dirty.py`, `store/documents_dirty_persist.py`, `store/edge_doc_contribution.py`, `store/edge_rebuild.py`, `store/edge_sync.py`, `store/field_set_drift.py`, `store/model_node.py`, `store/ops.py`, `store/section_doc_contribution.py`, `store/section_paths.py`, `store/section_sync.py`

### Reglas, estados y política (23)

`api/documents/on_write_gate.py`, `api/edges/apply_effects.py`, `api/edges/edges_blocked.py`, `api/edges/edges_holding.py`, `api/rules/builtin_tag_findings.py`, `api/rules/dirty_set.py`, `api/rules/fixpoint.py`, `api/rules/rule_graph.py`, `api/rules/rule_reach.py`, `api/rules/rule_subjects.py`, `api/rules/rule_view.py`, `api/rules/rule_writes.py`, `api/rules/rules_check.py`, `api/rules/rules_explain.py`, `api/rules/rules_on_check.py`, `api/rules/rules_on_transition.py`, `api/rules/rules_on_write.py`, `api/stores/declared_files.py`, `api/stores/judge_findings.py`, `api/stores/policy.py`, `api/stores/policy_subject.py`, `api/views/view_rules.py`, `api/views/view_transitions.py`

### Relaciones declaradas (15)

`api/documents/batch_edges.py`, `api/edges/builtin_relation_writes.py`, `api/edges/check_edges.py`, `api/edges/document_edge.py`, `api/edges/document_edges.py`, `api/edges/edge_effects.py`, `api/edges/referrer.py`, `api/edges/referrers.py`, `api/edges/relations_init_report.py`, `api/edges/rewrite_plan.py`, `api/edges/rewrite_references.py`, `api/edges/rewrite_report.py`, `api/edges/rewrite_values.py`, `api/edges/unresolved_references.py`, `api/stores/doc_ref_status.py`

### Kernel: árboles (14)

`api/documents/heading_scan.py`, `api/model_drafts/source_editing.py`, `api/records/extract.py`, `api/segments/build_document_segments.py`, `api/segments/build_extraction_segments.py`, `api/segments/document_segments.py`, `api/segments/extract_markdown_segments.py`, `api/segments/extracted_field.py`, `api/segments/extraction_segments.py`, `api/segments/field_segment.py`, `api/segments/literal_segment.py`, `api/segments/segment.py`, `api/segments/segment_display.py`, `api/segments/text_range.py`

### Varios stores y migración (13)

`api/edges/relation_models.py`, `api/model_registry/federated_lookup.py`, `api/model_registry/federated_registration.py`, `api/model_registry/inherit_model.py`, `api/stores/ambiguous_document.py`, `api/stores/doc_ref.py`, `api/stores/link_store.py`, `api/stores/linked_store.py`, `api/stores/migrate_layout.py`, `api/stores/store_links.py`, `api/stores/unlink_store.py`, `api/views/view_nodes.py`, `store/model_origin.py`

### Lo que se hace con git (11)

`api/documents/document_history.py`, `api/stores/branch_stores.py`, `api/stores/conflict_sides.py`, `api/stores/derived_recovery.py`, `api/stores/ensure_merge_driver.py`, `api/stores/gitignore_lines.py`, `api/stores/gitignore_policy.py`, `api/stores/merge_driver.py`, `api/stores/merge_driver_install.py`, `api/stores/store_file_merge.py`, `store/diagnostics_models/text_history.py`

### Cara (10)

`api/actor.py`, `api/documents/data_values.py`, `api/documents/document_ast.py`, `api/documents/document_ir_serialization.py`, `api/documents/document_render.py`, `api/documents/document_serialization.py`, `api/edges/edge_serialization.py`, `api/records/record_serialization.py`, `api/schema/store_schema.py`, `api/segments/segment_nodes.py`

### Kernel: anclaje (9)

`api/anchors/anchor_docs.py`, `api/anchors/anchor_report.py`, `api/anchors/check_anchors.py`, `api/anchors/check_doc_anchors.py`, `api/anchors/reconnect.py`, `api/anchors/record_anchor.py`, `api/anchors/resolve_pointers.py`, `api/documents/doc_anchor_pinning.py`, `store/diagnostics_models/verdict_notes.py`

### Notaciones y vistas (9)

`api/segments/segment_enrichment.py`, `api/views/list_views.py`, `api/views/run_view.py`, `api/views/view_groups.py`, `api/views/view_links.py`, `api/views/view_reading.py`, `api/views/view_revision.py`, `api/views/view_rows.py`, `api/views/view_source.py`

### Semántica (7)

`api/anchors/tag_reach.py`, `api/rules/builtin_tag_rules.py`, `api/stores/tag_namespace.py`, `api/tags/tag_check.py`, `api/tags/tag_evaluation.py`, `api/tags/tag_folder.py`, `api/tags/tag_tree.py`

### Enlaces en el texto (5)

`api/documents/move_path_links.py`, `api/records/ast_target.py`, `api/segments/composition_piece.py`, `api/segments/composition_spec.py`, `api/segments/source_ref.py`

### Fachada (5)

`api/graph/execute.py`, `api/graph/neighborhood.py`, `api/journal.py`, `api/schema/field_description.py`, `api/stores/migrate_hash_names.py`

### Kernel: consultas y reglas (3)

`api/documents/select_documents.py`, `api/documents/selector.py`, `api/records/record_filters.py`

### Análisis del grafo (3)

`api/graph/analyze.py`, `api/graph/traverse.py`, `api/views/view_edges.py`

### Código a documentos (2)

`api/code/code_facts.py`, `api/code/requested_files.py`

### Kernel: interfaz con git (1)

`store/package_version.py`

