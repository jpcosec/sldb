import logging
from sldb.api.records.search_record import SearchRecord
from .flatten import flatten_payload
from .map_fields import _map_fields_to_sections
from .utils import _slugify
from .build_ir import build_document_ir
from .extract import extract_sections

logger = logging.getLogger(__name__)

def _process_existing_doc(doc, doc_path, model_sections, records):
    doc_template = getattr(doc.model_type, "__template__", None)
    sections_idx = model_sections.get(doc.model_name)
    doc_sections = None
    if sections_idx is not None:
        doc_sections = next((ds for ds in sections_idx.documents if ds.doc_name == doc.name), None)
    if doc_sections is not None and doc_sections.sections:
        _process_doc_sections(doc, doc_sections.sections, doc_template, records)
    else:
        if doc_sections is None: logger.warning("No persisted sections for '%s', rebuilding IR from markdown", doc.name)
        _rebuild_from_markdown(doc, doc_path, doc_template, records)

def _process_doc_sections(doc, sections, doc_template, records):
    for sec in sections:
        slug = sec.slug or _slugify(sec.title)
        _add_section_record(doc, sec, slug, sec.breadcrumbs, records)
    known = set(name for name, _ in flatten_payload(doc.payload))
    field_section_map = _map_fields_to_sections(doc_template, sections, known_fields=known) if doc_template else {}
    for field_path, value in flatten_payload(doc.payload):
        _add_field_record(doc, field_path, value, field_section_map.get(field_path), records)

def _rebuild_from_markdown(doc, doc_path, doc_template, records):
    ir = build_document_ir(
        {"store": doc.store_name, "model": doc.model_name, "name": doc.name, "path": doc.path, "payload": doc.payload, "semantic_tags": doc.semantic_tags},
        doc_path.read_text(encoding="utf-8"), template=doc_template,
    )
    context_by_path = {entry.path: entry.model_dump(mode="json") for entry in ir.context_index}
    field_section_map = {node.field_path: node.owning_section for node in ir.nodes if node.kind == "field" and node.field_path}
    _add_rebuilt_sections(doc, doc_path, context_by_path, records)
    for field_path, value in flatten_payload(doc.payload):
        _add_field_record(doc, field_path, value, field_section_map.get(field_path), records)

def _add_rebuilt_sections(doc, doc_path, context_by_path, records):
    for section in extract_sections(doc_path.read_text(encoding="utf-8")):
        context_entry = context_by_path.get(section.path, {})
        _add_rebuilt_section_record(doc, section, context_entry, records)

def _add_section_record(doc, sec, slug, breadcrumbs, records):
    records.append(SearchRecord(
        kind="section", store_name=doc.store_name, name=slug,
        physical=[sec.title, slug, sec.path, doc.path], semantic=list(doc.semantic_tags),
        payload={"level": sec.level, "line_start": sec.line_start, "line_end": sec.line_end, "breadcrumbs": list(breadcrumbs)},
        model_name=doc.model_name, doc_name=doc.name, path=f"{doc.path}#{sec.path}", title=sec.title, about=list(sec.about),
    ))

def _add_rebuilt_section_record(doc, section, context_entry, records):
    records.append(SearchRecord(
        kind="section", store_name=doc.store_name, name=section.slug,
        physical=[section.title, section.slug, section.path, doc.path], semantic=list(doc.semantic_tags),
        payload={"level": section.level, "line_start": section.line_start, "line_end": section.line_end, "breadcrumbs": context_entry.get("breadcrumbs", [])},
        model_name=doc.model_name, doc_name=doc.name, path=f"{doc.path}#{section.path}", title=section.title, about=context_entry.get("about", []),
    ))

def _add_field_record(doc, field_path, value, owning_section, records):
    records.append(SearchRecord(
        kind="field", store_name=doc.store_name, name=field_path,
        physical=[field_path, doc.name, doc.path, doc.model_name], semantic=list(doc.semantic_tags),
        payload=doc.payload, value=value, model_name=doc.model_name, doc_name=doc.name,
        field_path=field_path, path=f"{doc.path}:{field_path}", owning_section=owning_section,
    ))
