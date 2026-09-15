# SLDB Architecture Map

Historical dependency snapshot. Entries such as `nldb.__main__` and `sldb.cli.graph` refer to an earlier source tree; this file is not a current import map. See the [verified source map](architecture/current-source-tree.md). Regenerating the exhaustive dependency map remains a [documentation gap](documentation-review.md).

## Modules

### `nldb.__main__`
No internal dependencies.

### `sldb.__main__`
Dependencies:
- sldb.cli.main

### `sldb.cli.commands.ast`
Dependencies:
- sldb.cli.graph.ast_for_target

### `sldb.cli.commands.basic`
Dependencies:
- sldb.cli.utils.read_text
- sldb.cli.utils.write_text
- sldb.cli.utils.resolve_model_ref
- sldb.runtime.validation.extract_model_data
- sldb.runtime.validation.render_model_markdown
- sldb.runtime.validation.validate_model_data_roundtrip
- sldb.runtime.validation.validate_model_input_roundtrip

### `sldb.cli.commands.doc`
Dependencies:
- sldb.cli.utils.get_store_context
- sldb.cli.utils.registered_model
- sldb.cli.utils.resolve_model_ref
- sldb.runtime.validation.render_model_markdown
- sldb.runtime.validation.validate_model_input_roundtrip
- sldb.store.ops.track_document
- sldb.core.exceptions.SLDBValidationError
- sldb.core.exceptions.SLDBASTError
- sldb.core.exceptions.SLDBError
- sldb.store.io.load_store_index
- sldb.store.io.load_models_index
- sldb.store.io.load_documents_index
- sldb.store.io.save_documents_index
- sldb.store.io.save_models_index
- sldb.store.io.store_lock
- sldb.store.hashing.hash_text
- sldb.store.hashing.hash_fields
- sldb.store.semantic.rebuild_semantic_indexes
- sldb.store.ops.cascade_hash_a
- sldb.store.io.load_documents_index
- sldb.store.io.load_models_index
- sldb.store.io.load_store_index
- sldb.store.io.save_documents_index
- sldb.store.io.save_models_index
- sldb.store.io.store_lock
- sldb.store.hashing.hash_documents_index
- sldb.store.ops.cascade_hash_a
- sldb.store.semantic.rebuild_sections_indexes
- sldb.store.semantic.rebuild_semantic_indexes

### `sldb.cli.commands.docs`
Dependencies:
- sldb.cli.commands.doc.DocCLI
- sldb.cli.commands.explore.ExploreCLI
- sldb.cli.commands.links.LinkCLI
- sldb.cli.graph.ast_for_target
- sldb.cli.utils.get_store_context
- sldb.store.io.load_documents_index
- sldb.store.io.load_models_index
- sldb.store.io.load_store_index

### `sldb.cli.commands.explore`
No internal dependencies.

### `sldb.cli.commands.faq`
No internal dependencies.

### `sldb.cli.commands.fields`
Dependencies:
- sldb.cli.graph.query_field_records
- sldb.cli.utils.deep_delete
- sldb.cli.utils.deep_get
- sldb.cli.utils.deep_set
- sldb.cli.utils.ensure_list
- sldb.cli.utils.get_store_context
- sldb.cli.utils.parse_data_value
- sldb.cli.utils.registered_model
- sldb.cli.utils.resolve_model_ref
- sldb.runtime.validation.render_model_markdown
- sldb.runtime.validation.validate_model_input_roundtrip
- sldb.store.hashing.hash_fields
- sldb.store.hashing.hash_text
- sldb.store.io.load_documents_index
- sldb.store.io.load_models_index
- sldb.store.io.load_store_index
- sldb.store.io.save_documents_index
- sldb.store.io.save_models_index
- sldb.store.io.store_lock
- sldb.store.ops.cascade_hash_a
- sldb.store.query.load_runtime_documents
- sldb.store.semantic.rebuild_semantic_indexes

### `sldb.cli.commands.find`
Dependencies:
- sldb.cli.graph.SearchRecord
- sldb.cli.graph.iter_search_records
- sldb.cli.graph.search_records
- sldb.store.query_engine.filter._where_matches
- sldb.cli.utils.resolve_model_ref

### `sldb.cli.commands.help`
No internal dependencies.

### `sldb.cli.commands.inbox`
Dependencies:
- sldb.cli.utils.get_store_context
- sldb.cli.utils.registered_model
- sldb.cli.utils.resolve_model_ref
- sldb.core.exceptions.SLDBStoreError
- sldb.core.exceptions.SLDBValidationError
- sldb.runtime.validation.validate_model_input_roundtrip
- sldb.store.layout.project_root
- sldb.store.ops.track_document
- sldb.store.resolver.find_local_store

### `sldb.cli.commands.init`
Dependencies:
- sldb.core.exceptions.SLDBError

### `sldb.cli.commands.legacy`
Dependencies:
- sldb.cli.commands.links.LinkCLI
- sldb.cli.commands.query.QueryCLI

### `sldb.cli.commands.links`
Dependencies:
- sldb.cli.utils.get_store_context
- sldb.cli.utils.write_text
- sldb.links.compose_document
- sldb.links.recover_links
- sldb.links.resolve_document_input

### `sldb.cli.commands.model`
Dependencies:
- sldb.cli.utils.get_store_context
- sldb.cli.utils.resolve_model_ref
- sldb.store.hashing.hash_documents_index
- sldb.store.hashing.hash_fields
- sldb.store.hashing.hash_text
- sldb.store.io.load_documents_index
- sldb.store.io.load_models_index
- sldb.store.io.load_store_index
- sldb.store.io.save_documents_index
- sldb.store.io.save_models_index
- sldb.store.io.store_lock
- sldb.store.layout.documents_index_relpath
- sldb.store.layout.models_index_relpath
- sldb.store.models.DocumentsIndex
- sldb.store.models.ModelEntry
- sldb.store.models.ModelsIndex
- sldb.store.ops.cascade_hash_a
- sldb.store.semantic.rebuild_semantic_indexes
- sldb.store.semantic_tags.flatten_model_semantics
- sldb.core.exceptions.SLDBModelError
- sldb.core.exceptions.SLDBError

### `sldb.cli.commands.models`
Dependencies:
- sldb.cli.commands.model.ModelCLI
- sldb.cli.graph.ast_for_target
- sldb.cli.utils.get_store_context
- sldb.cli.utils.parse_data_value
- sldb.cli.utils.read_text
- sldb.cli.utils.resolve_model_ref
- sldb.cli.utils.write_text
- sldb.core.exceptions.SLDBModelDraftError
- sldb.core.exceptions.SLDBModelEditError
- sldb.core.exceptions.SLDBModelError
- sldb.core.exceptions.SLDBValidationError
- sldb.runtime.validation.Validator
- sldb.runtime.validation.validate_model_input_roundtrip
- sldb.store.io.load_documents_index
- sldb.store.io.load_models_index
- sldb.store.io.load_store_index

### `sldb.cli.commands.predicates`
Dependencies:
- sldb.cli.utils.get_store_context
- sldb.core.exceptions.SLDBStoreError
- sldb.store.io.load_store_index
- sldb.store.io.save_store_index
- sldb.store.models.PredicateEntry
- sldb.store.predicates.validate_predicate
- sldb.store.predicates.validate_predicates

### `sldb.cli.commands.query`
Dependencies:
- sldb.cli.utils.get_store_context
- sldb.cli.utils.resolve_model_ref
- sldb.store.query.find_semantic
- sldb.store.query.find_structural
- sldb.store.query.get_global_semantic
- sldb.store.query.get_semantic
- sldb.store.query.get_structural
- sldb.store.query.glob_semantic
- sldb.store.query.glob_structural
- sldb.store.query.list_global_semantic
- sldb.store.query.list_semantic
- sldb.store.query.list_structural
- sldb.core.exceptions.SLDBStoreError

### `sldb.cli.commands.sections`
Dependencies:
- sldb.cli.graph._map_fields_to_sections
- sldb.cli.graph.build_document_ir
- sldb.cli.graph.flatten_payload
- sldb.cli.graph.iter_search_records
- sldb.cli.graph.resolve_runtime_doc
- sldb.cli.graph.search_records
- sldb.cli.utils.get_store_context
- sldb.store.io.load_documents_index
- sldb.store.io.load_models_index
- sldb.store.io.load_sections_index
- sldb.store.io.load_store_index
- sldb.store.models.SectionContextRecord
- sldb.cli.commands.find.FindCLI

### `sldb.cli.commands.store`
Dependencies:
- sldb.cli.utils.get_store_context
- sldb.cli.utils.resolve_model_ref
- sldb.core.exceptions.SLDBError
- sldb.core.exceptions.SLDBStoreError
- sldb.store.hashing.hash_documents_index
- sldb.store.hashing.hash_fields
- sldb.store.hashing.hash_text
- sldb.store.io.load_documents_index
- sldb.store.io.load_models_index
- sldb.store.io.load_semantic_dag
- sldb.store.io.load_store_index
- sldb.store.io.save_documents_index
- sldb.store.io.save_models_index
- sldb.store.io.save_semantic_dag
- sldb.store.io.save_semantic_index
- sldb.store.io.save_store_index
- sldb.store.io.store_lock
- sldb.store.layout.store_exists
- sldb.store.models.SemanticDAG
- sldb.store.models.StoreEntry
- sldb.store.models.StoreIndex
- sldb.store.models.SemanticIndex
- sldb.store.predicates.default_predicates
- sldb.store.ops.cascade_hash_a
- sldb.store.semantic.RebuildReport
- sldb.store.semantic.rebuild_sections_indexes
- sldb.store.semantic.rebuild_semantic_indexes
- sldb.store.diagnostics.diagnose_store

### `sldb.cli.commands.stores`
Dependencies:
- sldb.cli.commands.store.StoreCLI
- sldb.cli.utils.get_store_context
- sldb.cli.utils.resolve_model_ref
- sldb.cli.utils.write_text
- sldb.store.export.export_kgdb_semantic_payload
- sldb.store.io.load_store_index

### `sldb.cli.graph`
Dependencies:
- sldb.cli.utils.get_store_context
- sldb.cli.utils.resolve_model_ref
- sldb.store.layout.project_root
- sldb.core.ast.AST_Handler
- sldb.core.contracts.MARKER_PATTERN
- sldb.core.contracts.parse_marker
- sldb.core.ir.DocumentContext
- sldb.core.ir.DocumentIR
- sldb.core.ir.GraphEdge
- sldb.core.ir.GraphView
- sldb.core.ir.MeaningNode
- sldb.core.ir.SectionContextEntry
- sldb.core.ir.SourceSpan
- sldb.core.ir.SurfaceNode
- sldb.store.io.load_documents_index
- sldb.store.io.load_models_index
- sldb.store.io.load_sections_index
- sldb.store.io.load_store_index
- sldb.store.models.DocSections
- sldb.store.models.SectionContextRecord
- sldb.store.models.SectionsIndex
- sldb.store.query.load_runtime_documents

### `sldb.cli.main`
Dependencies:
- sldb.cli.parser.build_parser
- sldb.cli.commands.help.SHORT_ARGPARSE_HELP
- sldb.core.exceptions.SLDBError
- sldb.cli.commands.ast.ASTCLI
- sldb.cli.commands.basic.BasicCLI
- sldb.cli.commands.docs.DocsCLI
- sldb.cli.commands.explore.ExploreCLI
- sldb.cli.commands.fields.FieldsCLI
- sldb.cli.commands.find.FindCLI
- sldb.cli.commands.faq.FAQCLI
- sldb.cli.commands.help.HelpCLI
- sldb.cli.commands.init.InitCLI
- sldb.cli.commands.inbox.InboxCLI
- sldb.cli.commands.legacy.LegacyCLI
- sldb.cli.commands.links.LinkCLI
- sldb.cli.commands.models.ModelsCLI
- sldb.cli.commands.predicates.PredicatesCLI
- sldb.cli.commands.query.QueryCLI
- sldb.cli.commands.sections.SectionsCLI
- sldb.cli.commands.stores.StoresCLI
- sldb.cli.commands.store.StoreCLI
- sldb.cli.commands.model.ModelCLI
- sldb.cli.commands.doc.DocCLI

### `sldb.cli.parser`
No internal dependencies.

### `sldb.cli.utils`
Dependencies:
- sldb.core.exceptions.SLDBModelError
- sldb.models.structured_doc.StructuredNLDoc
- sldb.store.resolver.global_store_path
- sldb.store.resolver.find_local_store
- sldb.core.exceptions.SLDBStoreError
- sldb.store.layout.project_root
- sldb.store.layout.store_exists
- sldb.store.migration.migrate_store_layout
- sldb.store.resolver.find_local_store
- sldb.store.layout.project_root
- sldb.store.layout.store_exists
- sldb.store.io.load_store_index
- sldb.core.exceptions.SLDBStoreError
- sldb.store.io.load_store_index
- sldb.core.exceptions.SLDBStoreError
- sldb.store.resolver.find_local_store
- sldb.store.layout.project_root
- sldb.store.layout.store_exists
- sldb.store.io.load_store_index
- sldb.store.io.load_store_index
- sldb.store.io.save_documents_index
- sldb.store.io.save_models_index
- sldb.store.io.store_lock
- sldb.store.layout.documents_index_relpath
- sldb.store.layout.models_index_relpath
- sldb.store.models.DocumentsIndex
- sldb.store.models.ModelEntry
- sldb.store.models.ModelsIndex
- sldb.store.ops.cascade_hash_a
- sldb.store.semantic_tags.flatten_model_semantics

### `sldb.core.ast`
Dependencies:
- sldb.core.node.SLDBNode

### `sldb.core.contracts`
No internal dependencies.

### `sldb.core.data_extractor`
Dependencies:
- sldb.core.node.SLDBNode
- sldb.core.node_handler.SharedNodeHandler

### `sldb.core.exceptions`
No internal dependencies.

### `sldb.core.handlers.base`
Dependencies:
- sldb.core.node.SLDBNode

### `sldb.core.handlers.list`
Dependencies:
- sldb.core.handlers.base.BaseNodeHandler
- sldb.core.handlers.utils.parse_marker
- sldb.core.node.SLDBNode

### `sldb.core.handlers.router`
Dependencies:
- sldb.core.handlers.list.ListNodeHandler
- sldb.core.handlers.table.TableNodeHandler
- sldb.core.handlers.text.TextNodeHandler
- sldb.core.handlers.yaml.YamlNodeHandler
- sldb.core.node.SLDBNode

### `sldb.core.handlers.table`
Dependencies:
- sldb.core.handlers.base.BaseNodeHandler
- sldb.core.handlers.utils.parse_marker
- sldb.core.node.SLDBNode
- sldb.core.handlers.text.build_text_pattern

### `sldb.core.handlers.text`
Dependencies:
- sldb.core.handlers.base.BaseNodeHandler
- sldb.core.handlers.utils.parse_marker
- sldb.core.node.SLDBNode

### `sldb.core.handlers.utils`
Dependencies:
- sldb.core.contracts.Marker

### `sldb.core.handlers.yaml`
Dependencies:
- sldb.core.exceptions.SLDBASTError
- sldb.core.handlers.base.BaseNodeHandler
- sldb.core.handlers.utils.parse_marker
- sldb.core.node.SLDBNode

### `sldb.core.ingest.engine`
No internal dependencies.

### `sldb.core.ingest.manifest`
No internal dependencies.

### `sldb.core.ingest.scanner`
No internal dependencies.

### `sldb.core.ir`
No internal dependencies.

### `sldb.core.node`
No internal dependencies.

### `sldb.core.node_handler`
Dependencies:
- sldb.core.handlers.router.SharedNodeHandler

### `sldb.core.renderer`
Dependencies:
- sldb.core.ast.AST_Handler
- sldb.core.handlers.router.SharedNodeHandler
- sldb.core.renderer_engine.list.ListRenderer
- sldb.core.renderer_engine.table.TableRenderer
- sldb.core.renderer_engine.yaml.YamlRenderer
- sldb.models.structured_doc.StructuredNLDoc

### `sldb.core.renderer_engine.base`
Dependencies:
- sldb.core.handlers.utils.parse_marker
- sldb.core.renderer_engine.python_expr.PythonExpressionRenderer

### `sldb.core.renderer_engine.list`
Dependencies:
- sldb.core.renderer_engine.base.BaseRenderer

### `sldb.core.renderer_engine.python_expr`
Dependencies:
- sldb.runtime.config.python_expression_is_allowed

### `sldb.core.renderer_engine.table`
Dependencies:
- sldb.core.renderer_engine.base.BaseRenderer

### `sldb.core.renderer_engine.yaml`
Dependencies:
- sldb.core.renderer_engine.base.BaseRenderer
- sldb.core.handlers.utils.parse_marker

### `sldb.core.template_extractor`
Dependencies:
- sldb.core.exceptions.SLDBASTError
- sldb.core.node.SLDBNode
- sldb.core.node_handler.SharedNodeHandler

### `sldb.examples.pandoc_cv.cv_model`
Dependencies:
- sldb.StructuredNLDoc

### `sldb.examples.reference_bundle.guide_model`
Dependencies:
- sldb.StructuredNLDoc

### `sldb.links`
Dependencies:
- sldb.store.layout.project_root
- sldb.store.io.load_documents_index
- sldb.store.io.load_models_index
- sldb.store.io.load_store_index
- sldb.store.predicates.predicate_axes

### `sldb.models.structured_doc`
Dependencies:
- sldb.runtime.validation.extract_model_data

### `sldb.runtime.config`
No internal dependencies.

### `sldb.runtime.validation`
Dependencies:
- sldb.core.ast.AST_Handler
- sldb.core.data_extractor.DataExtractor
- sldb.core.renderer.SLDBRenderer
- sldb.core.template_extractor.TemplateExtractor
- sldb.models.structured_doc.StructuredNLDoc
- sldb.core.ast.AST_Handler
- sldb.core.data_extractor.DataExtractor
- sldb.core.template_extractor.TemplateExtractor
- sldb.core.renderer.SLDBRenderer
- sldb.models.structured_doc.StructuredNLDoc

### `sldb.store.diagnostics`
Dependencies:
- sldb.models.structured_doc.StructuredNLDoc
- sldb.store.layout.project_root
- sldb.store.hashing.hash_documents_index
- sldb.store.hashing.hash_fields
- sldb.store.hashing.hash_models_layer
- sldb.store.hashing.hash_text
- sldb.store.io.load_documents_index
- sldb.store.io.load_models_index
- sldb.store.io.load_store_index
- sldb.store.models.ModelsIndex
- sldb.store.diagnostics_models.DiagnosisNote
- sldb.store.diagnostics_models.DocumentDiagnosis
- sldb.store.diagnostics_models.ModelDiagnosis
- sldb.store.diagnostics_models.StoreDiagnosis
- sldb.cli.utils.resolve_model_ref

### `sldb.store.diagnostics_models`
No internal dependencies.

### `sldb.store.export`
Dependencies:
- sldb.store.io.load_documents_index
- sldb.store.io.load_models_index
- sldb.store.io.load_sections_index
- sldb.store.io.load_semantic_dag
- sldb.store.io.load_store_index
- sldb.store.io.store_lock
- sldb.store.layout.semantic_dag_path
- sldb.store.layout.semantic_index_path
- sldb.store.layout.store_index_path
- sldb.store.semantic.rebuild_sections_indexes
- sldb.store.semantic.rebuild_semantic_indexes

### `sldb.store.hashing`
Dependencies:
- sldb.models.structured_doc.StructuredNLDoc
- sldb.runtime.validation.extract_model_data
- sldb.store.models.DocumentsIndex
- sldb.store.models.ModelsIndex

### `sldb.store.io`
Dependencies:
- sldb.core.exceptions.SLDBStoreError
- sldb.store.layout.legacy_semantic_dag_path
- sldb.store.layout.legacy_semantic_index_path
- sldb.store.layout.legacy_store_index_path
- sldb.store.layout.lock_path
- sldb.store.layout.semantic_dag_path
- sldb.store.layout.semantic_index_path
- sldb.store.layout.store_index_path
- sldb.store.models.DocumentsIndex
- sldb.store.models.ModelsIndex
- sldb.store.models.SectionsIndex
- sldb.store.models.SemanticDAG
- sldb.store.models.SemanticIndex
- sldb.store.models.StoreIndex

### `sldb.store.layout`
No internal dependencies.

### `sldb.store.migration`
Dependencies:
- sldb.store.io.load_documents_index
- sldb.store.io.load_models_index
- sldb.store.io.load_sections_index
- sldb.store.io.load_semantic_dag
- sldb.store.io.load_semantic_index
- sldb.store.io.load_store_index
- sldb.store.io.save_documents_index
- sldb.store.io.save_models_index
- sldb.store.io.save_sections_index
- sldb.store.io.save_semantic_dag
- sldb.store.io.save_semantic_index
- sldb.store.io.save_store_index
- sldb.store.layout.documents_index_relpath
- sldb.store.layout.models_index_relpath
- sldb.store.layout.sections_index_relpath
- sldb.store.layout.store_index_path

### `sldb.store.models`
No internal dependencies.

### `sldb.store.ops`
Dependencies:
- sldb.store.hashing.hash_documents_index
- sldb.store.hashing.hash_fields
- sldb.store.hashing.hash_models_layer
- sldb.store.hashing.hash_text
- sldb.store.io.load_documents_index
- sldb.store.io.load_models_index
- sldb.store.io.save_documents_index
- sldb.store.io.save_models_index
- sldb.store.io.save_store_index
- sldb.store.io.store_lock
- sldb.store.models.DocumentEntry
- sldb.store.models.StoreIndex
- sldb.store.semantic.rebuild_semantic_indexes
- sldb.core.exceptions.SLDBStoreError

### `sldb.store.predicates`
Dependencies:
- sldb.store.models.PredicateEntry

### `sldb.store.query`
Dependencies:
- sldb.runtime.validation.extract_model_data
- sldb.store.layout.project_root
- sldb.store.layout.store_exists
- sldb.store.io.load_documents_index
- sldb.store.io.load_models_index
- sldb.store.io.load_store_index
- sldb.store.query_engine.models.RuntimeDocument
- sldb.store.query_engine.structural.list_structural
- sldb.store.query_engine.structural.get_structural
- sldb.store.query_engine.structural_queries.glob_structural
- sldb.store.query_engine.structural_queries.find_structural
- sldb.store.query_engine.semantic.list_semantic
- sldb.store.query_engine.semantic.get_semantic
- sldb.store.query_engine.semantic.glob_semantic
- sldb.store.query_engine.semantic.find_semantic
- sldb.store.query_engine.global_semantic.get_global_semantic
- sldb.store.query_engine.global_semantic.list_global_semantic

### `sldb.store.query_engine.filter`
Dependencies:
- sldb.store.query_engine.models.RuntimeDocument

### `sldb.store.query_engine.global_semantic`
Dependencies:
- sldb.store.io.load_semantic_dag
- sldb.store.query.load_runtime_documents

### `sldb.store.query_engine.models`
No internal dependencies.

### `sldb.store.query_engine.semantic`
Dependencies:
- sldb.store.query_engine.semantic_utils._local_semantic_docs
- sldb.store.query_engine.semantic_utils._semantic_children
- sldb.store.query_engine.semantic_utils._match_semantic_pattern
- sldb.store.query_engine.filter._where_matches

### `sldb.store.query_engine.semantic_utils`
Dependencies:
- sldb.store.layout.project_root
- sldb.store.io.load_semantic_index
- sldb.store.query.load_runtime_documents
- sldb.store.query_engine.models.RuntimeDocument
- sldb.store.semantic.rebuild_semantic_indexes

### `sldb.store.query_engine.structural`
Dependencies:
- sldb.store.io.load_store_index
- sldb.store.query.load_runtime_documents

### `sldb.store.query_engine.structural_queries`
Dependencies:
- sldb.store.query_engine.structural._model_scope_docs
- sldb.store.query_engine.filter._where_matches

### `sldb.store.resolver`
Dependencies:
- sldb.store.layout.store_exists

### `sldb.store.semantic`
Dependencies:
- sldb.runtime.validation.extract_model_data
- sldb.store.io.load_documents_index
- sldb.store.io.load_models_index
- sldb.store.io.load_sections_index
- sldb.store.io.load_semantic_dag
- sldb.store.io.load_store_index
- sldb.store.io.save_documents_index
- sldb.store.io.save_models_index
- sldb.store.io.save_sections_index
- sldb.store.io.save_semantic_dag
- sldb.store.io.save_semantic_index
- sldb.store.layout.sections_index_relpath
- sldb.store.models.DocSections
- sldb.store.models.SectionContextRecord
- sldb.store.models.SectionsIndex
- sldb.store.models.SemanticDAG
- sldb.store.models.SemanticDocumentRecord
- sldb.store.models.SemanticIndex
- sldb.store.models.SemanticNode
- sldb.store.semantic_tags.collect_document_semantic_tags
- sldb.store.semantic_tags._prefix_edges

### `sldb.store.semantic_tags`
No internal dependencies.

## CLI Surface (`sldb.cli.parser`)
- **Primary user entrypoints**: `find` (structural and semantic queries)
- **Legacy/Raw entrypoints**: `ls`, `get`, `glob`, `find`
- **Link/Composition entrypoints**: `recover`, `compose`
- **State management (hidden)**: `store` (init, add, check, update, semantic-map), `model` (add, update), `doc` (add, track, update, untrack)

## Hotspots & Import Cycles
- **Hotspots**:
  - `sldb.store.io`: Centralized point for all reads/writes. Depended on by multiple systems.
  - `sldb.store.hashing`: Core mechanism for structural integrity.
  - `sldb.runtime.validation`: Coordinates extraction, templating, rendering.
- **Cycles**: 
  - `sldb.runtime.validation` depends on `sldb.models.structured_doc`, which in turn relies on `sldb.runtime.validation.extract_model_data`. (Noticeable cyclic behavior typically mitigated by deferred/local imports).
  - `sldb.store.semantic` updates semantic models, but depends heavily on raw `io` operations which also fetch semantic data.

## Subsistemas Reales
1. **Core Runtime & Handlers**: `sldb.core.*` (AST parsing, YAML/Python handlers, templating, Markdown rendering).
2. **Store Management**: `sldb.store.*` (Hashing, disk layout, validation, diagnostics, export/migration).
3. **Query Engine**: `sldb.store.query_engine.*` (Structural/Semantic querying, global scopes, runtime doc mapping).
4. **CLI**: `sldb.cli.*` (User surface).

## Mapa Inicial para spec2viz
This map will serve as the baseline for the future `spec2viz` modularization, decoupling the query engine from the core store io operations, and lifting the CLI into its own well-defined layer.
