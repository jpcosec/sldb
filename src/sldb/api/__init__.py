"""sldb's library API: the store, model and document operations the CLI performs, as functions.

Consumers (pron, kgdb, deskops...) call these instead of instantiating `sldb.cli` command
classes with fake argparse namespaces. Each operation that names a store opens it the way a
CLI command does (`open_store`), returns a pydantic model instead of printing, and raises
`sldb.core.exceptions` errors instead of exiting. Layering: `sldb.cli` -> `sldb.api` ->
`sldb.store` / `sldb.runtime` / `sldb.core`; nothing here imports `sldb.cli`.
"""

from __future__ import annotations

from sldb.api.documents.create_document import create_document
from sldb.api.documents.delete_document import delete_document
from sldb.api.documents import document_ast, build_document_ir_json, leaf_paths, runtime_document, extract_document_payload, render_document_markdown, render_model_template
from sldb.api.documents.runtime_documents import load_runtime_documents
from sldb.api.documents.document_reference import DocumentReference
from sldb.api.documents.document_serialization import serialize_document
from sldb.api.documents.payload_path_reading import deep_get, ensure_list
from sldb.api.documents.payload_path_writing import deep_delete, deep_set
from sldb.api.documents.payload_save import save_document_payload
from sldb.api.documents.track_document_file import track_document_file
from sldb.api.documents.untrack_document import untrack_document
from sldb.api.edges.check_edges import check_edges
from sldb.api.edges.edge_check_report import EdgeCheckReport
from sldb.api.edges.edge_reading import edge_node, edge_nodes_of_type, edges_from, edges_to, load_edge_index
from sldb.api.edges.edges_holding import edges_holding
from sldb.api.model_registry.remove_model import remove_model
from sldb.api.model_registry.inherit_model import inherit_model
from sldb.models.structured_doc import StructuredNLDoc
from sldb.api.edges.unresolved_references import unresolved_references
from sldb.store.edge_index.unresolved_reference import UnresolvedReference
from sldb.api.edges.edge_serialization import serialize_edge_node_record, serialize_edge_node_records, serialize_edge_record, serialize_edge_records
from sldb.api.edges.init_relations import init_relations
from sldb.api.edges.rebuild_edges import rebuild_edges
from sldb.api.edges.relations_init_report import RelationsInitReport
from sldb.api.journal import journal, verify_journal
from sldb.api.model_drafts.draft_document_check import DraftDocumentCheck
from sldb.api.model_drafts.draft_validation import promote_model_draft, validate_model_draft
from sldb.api.model_drafts.draft_validation_report import DraftValidationReport
from sldb.api.model_drafts.field_drafts import add_model_field, remove_model_field
from sldb.api.model_drafts.model_draft import ModelDraft
from sldb.api.model_drafts.model_source import ModelSource
from sldb.api.model_drafts.source_location import locate_model_source
from sldb.api.model_drafts.template_drafts import edit_model_template
from sldb.api.model_create.create_model import create_model
from sldb.api.model_create.field_decl import FieldDecl
from sldb.api.model_create.model_check import ModelCheck
from sldb.api.model_registry.add_model import add_model
from sldb.api.search import search
from sldb.api.where import where_matches
from sldb.store.query_engine.where_parse import WherePredicateError
from sldb.api.model_registry.describe_model import describe_model
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.model_registry.model_description import ModelDescription
from sldb.api.model_registry.model_document_summary import ModelDocumentSummary
from sldb.api.model_registry.model_field_summary import ModelFieldSummary
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.model_registry.model_registration import ModelRegistration
from sldb.api.model_registry.registered_model import RegisteredModel
from sldb.api.model_registry.reindex_model import reindex_model
from sldb.api.schema.describe_field import describe_field, describe_model_fields
from sldb.api.schema.field_description import FieldDescription
from sldb.api.segments import CompositionPiece, CompositionSpec, DocumentSegments, FieldSegment, LiteralSegment, Segment, SourceRef, build_document_segments
from sldb.api.stores.doc_ref import split_doc_ref
from sldb.api.stores.doc_ref_status import DocRefStatus
from sldb.api.stores.doc_status import doc_exists, doc_status
from sldb.api.stores.init_store import init_store
from sldb.api.stores.link_store import link_store
from sldb.api.stores.unlink_store import unlink_store
from sldb.api.stores.linked_store import LinkedStore
from sldb.api.stores.migrate_hash_names import migrate_store_hash_names
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_check import check_store
from sldb.api.stores.store_fingerprint import store_fingerprint
from sldb.api.stores.store_links import store_links
from sldb.api.stores.store_location import StoreLocation
from sldb.api.stores.store_update_report import StoreUpdateReport
from sldb.api.stores.update_store_indexes import update_store_indexes
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.edge_rebuild_report import EdgeRebuildReport
from sldb.store.edge_index.node_ids import anchor_node_id, bare, doc_node_id, field_node_id, kind, model_node_id, relation_type_node_id, section_node_id, tag_node_id
from sldb.store.journal import JournalEntry, JournalVerifyReport
from sldb.store.models.edge_node_record import EdgeNodeRecord
from sldb.store.models.edge_record import EdgeRecord
from sldb.store.models.document_hashes import DocumentHashes
from sldb.store.models.store_fingerprint import StoreFingerprint
from sldb.api.corpus import (
    Corpus,
    CorpusEntry,
    FieldEntry,
    FieldHit,
    FieldProjection,
    Hit,
    IndexProjection,
    field_id,
    split_field_id,
)

__all__ = [
    "Corpus", "CorpusEntry", "FieldEntry", "FieldHit", "FieldProjection",
    "Hit", "IndexProjection", "field_id", "split_field_id",
    "CompositionPiece", "CompositionSpec", "DocumentSegments", "FieldSegment",
    "LiteralSegment", "Segment", "SourceRef", "build_document_segments",
    "DocumentHashes", "DocumentReference", "DraftDocumentCheck", "DraftValidationReport",
    "EdgeCheckReport", "EdgeIndex", "EdgeNodeRecord", "EdgeRebuildReport",
    "EdgeRecord", "FieldDecl", "FieldDescription", "JournalEntry",
    "JournalVerifyReport", "LinkedStore", "ModelCheck", "ModelDescription",
    "ModelDocumentSummary", "ModelDraft", "ModelFieldSummary", "ModelRegistration",
    "ModelSource", "RegisteredModel", "RelationsInitReport", "StoreFingerprint",
    "StoreLocation", "StoreUpdateReport", "add_model", "add_model_field",
    "create_model", "anchor_node_id", "bare", "check_edges", "check_store",
    "store_fingerprint", "create_document", "deep_delete", "deep_get", "deep_set",
    "delete_document", "describe_field", "describe_model", "describe_model_fields",
    "doc_node_id", "document_ast", "edge_node", "edge_nodes_of_type", "edges_from",
    "edges_to", "edit_model_template", "ensure_list", "extract_document_payload",
    "field_node_id", "init_relations", "init_store", "journal", "kind", "link_store", "unlink_store",
    "load_edge_index", "leaf_paths", "load_runtime_documents", "migrate_store_hash_names",
    "load_registered_model", "locate_model_source", "model_node_id", "open_store",
    "promote_model_draft", "rebuild_edges", "reindex_model", "relation_type_node_id",
    "remove_model_field", "render_document_markdown", "render_model_template",
    "resolve_model_ref", "runtime_document", "save_document_payload", "search",
    "section_node_id", "serialize_document", "serialize_edge_node_records",
    "serialize_edge_records", "tag_node_id", "track_document_file", "untrack_document",
    "update_store_indexes", "validate_model_draft", "verify_journal",
    "DocRefStatus", "doc_exists", "doc_status", "split_doc_ref", "store_links",
    "WherePredicateError", "edges_holding", "remove_model", "where_matches", "inherit_model",
    "StructuredNLDoc", "UnresolvedReference", "unresolved_references",
]
