from typing import Any
from sldb.store.io import load_store_index, load_models_index, load_sections_index
from sldb.store.query import load_runtime_documents
from sldb.store.layout import project_root
from sldb.api.stores.open_store import open_store
from sldb.api.model_registry.model_reference import resolve_model_ref
from .flatten import flatten_payload
from .map_fields import _map_fields_to_sections
from .extract import extract_sections

def query_field_records(store_arg: str | None, pythonpath: str | None, field_ref: str, include_linked: bool = False) -> list[dict[str, Any]]:
    location = open_store(store_arg)
    store_path, root = location.store_path, location.project_root
    store_index = load_store_index(store_path)
    docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath, include_linked=include_linked)
    model_sections = _load_model_sections(store_index, root)
    results = []
    for doc in docs: _process_field_doc(doc, field_ref, model_sections, results)
    return results

def _load_model_sections(store_index, root):
    model_sections = {}
    for model_entry in store_index.models:
        models_idx = load_models_index(root / model_entry.models_index)
        if models_idx.sections_index:
            sections_path = root / models_idx.sections_index
            model_sections[model_entry.name] = load_sections_index(sections_path)
    return model_sections

def _process_field_doc(doc, field_ref, model_sections, results):
    matched_pairs = [(p, v) for p, v in flatten_payload(doc.payload) if p == field_ref or p.endswith(f".{field_ref}")]
    if not matched_pairs: return
    owning_section_map = _get_owning_section_map(doc, model_sections)
    for path, value in matched_pairs:
        results.append({
            "store": doc.store_name, "model": doc.model_name, "doc": doc.name,
            "path": doc.path, "field": path, "value": value, "owning_section": owning_section_map.get(path),
        })

def _get_owning_section_map(doc, model_sections):
    doc_template: str | None = getattr(doc.model_type, "__template__", None)
    if not doc_template: return {}
    sections_idx = model_sections.get(doc.model_name)
    doc_sections = next((ds for ds in sections_idx.documents if ds.doc_name == doc.name), None) if sections_idx else None
    if doc_sections is not None and doc_sections.sections:
        return _map_fields_to_sections(doc_template, doc_sections.sections)
    return _extract_from_path(doc, doc_template)

def _extract_from_path(doc, doc_template):
    doc_path = project_root(doc.store_path) / doc.path
    if doc_path.exists():
        sections = extract_sections(doc_path.read_text(encoding="utf-8"))
        return _map_fields_to_sections(doc_template, sections)
    return {}
