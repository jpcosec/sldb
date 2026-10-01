"""Record-level reads: the store seen as searchable store/model/doc/section/field records.

This is the machinery behind `sldb find`, `sldb ast` and `sldb sections`. It lives in
`sldb.api` because `sldb.api.search` and `sldb.api.document_ast` are library entry points:
the api layer must not import the CLI. `sldb.cli.graph_ops` re-exports these names for
existing importers.
"""

from .ast_target import ast_for_target
from .build_ast import build_store_ast
from .build_ir import build_document_ir
from .extract import extract_sections
from .fields import query_field_records
from .flatten import flatten_payload
from .iter_records import iter_search_records
from .map_fields import _field_template_line_map, _map_fields_to_sections
from .matches import search_records, _matches_term
from .record_filters import RecordFilters
from .record_serialization import select_keys, serialize_record, serialize_records
from .resolve import resolve_runtime_doc
from .runtime_doc_proxy import RuntimeDocProxy
from .search_record import SearchRecord
from .section_record import SectionRecord
from .utils import _slugify, _annotation_name, _to_surface_node, _about_terms

__all__ = [
    "RecordFilters", "RuntimeDocProxy", "SearchRecord", "SectionRecord",
    "ast_for_target", "build_document_ir", "build_store_ast", "extract_sections",
    "flatten_payload", "iter_search_records", "query_field_records",
    "resolve_runtime_doc", "search_records", "select_keys", "serialize_record",
    "serialize_records",
]
