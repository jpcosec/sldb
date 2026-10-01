"""Compatibility bridge: record reads now live in `sldb.api.records`.

Moved so `sldb.api.search` and `sldb.api.document_ast` stop importing the CLI, which
inverted the declared layering (`sldb.cli` -> `sldb.api` -> `sldb.store`/`sldb.core`).
New code should import from `sldb.api.records`.
"""

from sldb.api.records import (  # noqa: F401 - re-exported for existing importers
    SearchRecord,
    SectionRecord,
    _about_terms,
    _annotation_name,
    _field_template_line_map,
    _map_fields_to_sections,
    _matches_term,
    _slugify,
    _to_surface_node,
    ast_for_target,
    build_document_ir,
    build_store_ast,
    extract_sections,
    flatten_payload,
    iter_search_records,
    query_field_records,
    resolve_runtime_doc,
    search_records,
)
