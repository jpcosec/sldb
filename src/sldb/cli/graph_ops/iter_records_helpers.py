import logging
from pathlib import Path
from sldb.store.io import load_models_index, load_sections_index
from sldb.store.layout import project_root
from sldb.cli.search_record import SearchRecord
from .flatten import flatten_payload
from .map_fields import _map_fields_to_sections
from .utils import _slugify
from .build_ir import build_document_ir
from .extract import extract_sections
from .iter_records_docs import _process_existing_doc

logger = logging.getLogger(__name__)

def _load_model_sections(store_index, root, rebuild):
    model_sections = {}
    if not rebuild:
        for model_entry in store_index.models:
            models_idx = load_models_index(root / model_entry.models_index)
            if models_idx.sections_index:
                sections_path = root / models_idx.sections_index
                model_sections[model_entry.name] = load_sections_index(sections_path)
    return model_sections

def _build_store_records(store_path, root, store_index):
    records: list[SearchRecord] = [
        SearchRecord(
            kind="store", store_name="local", name="local", physical=[str(store_path), str(root), ".sldb"],
            semantic=[], payload={"linked_count": len(store_index.stores), "model_count": len(store_index.models)},
            path=str(store_path),
        )
    ]
    for entry in store_index.stores: _add_store_record(entry, records)
    return records

def _add_store_record(entry, records):
    records.append(SearchRecord(
        kind="store", store_name="local", name=entry.name, physical=[entry.name, entry.path],
        semantic=[], payload={"linked": True}, path=entry.path,
    ))

def _process_docs(runtime_docs, store_index, model_sections, records):
    seen_models: set[tuple[str, str]] = set()
    local_models = {entry.name: entry for entry in store_index.models}
    for doc in runtime_docs:
        _add_model_record(doc, local_models, seen_models, records)
        _add_doc_record(doc, records)
        _process_doc_details(doc, model_sections, records)

def _add_model_record(doc, local_models, seen_models, records):
    model_key = (doc.store_name, doc.model_name)
    if model_key not in seen_models:
        _do_add_model(doc, local_models.get(doc.model_name), records)
        seen_models.add(model_key)

def _do_add_model(doc, entry, records):
    semantics = list(getattr(entry, "semantics", [])) if entry else []
    records.append(SearchRecord(
        kind="model", store_name=doc.store_name, name=doc.model_name,
        physical=[doc.model_name, getattr(doc.model_type, "__module__", "")],
        semantic=semantics, payload={"field_count": len(doc.model_type.model_fields)}, # type: ignore[attr-defined]
        model_name=doc.model_name, path=getattr(entry, "path", None) if entry else None,
    ))

def _add_doc_record(doc, records):
    records.append(SearchRecord(
        kind="doc", store_name=doc.store_name, name=doc.name,
        physical=[doc.name, doc.path, f"{doc.model_name}/{doc.name}"],
        semantic=list(doc.semantic_tags), payload=doc.payload,
        model_name=doc.model_name, doc_name=doc.name, path=doc.path, model_type=doc.model_type,
    ))

def _process_doc_details(doc, model_sections, records):
    doc_path = Path(project_root(doc.store_path) / doc.path)
    if doc_path.exists():
        _process_existing_doc(doc, doc_path, model_sections, records)
    else:
        from .iter_records_docs import _add_field_record
        for field_path, value in flatten_payload(doc.payload):
            _add_field_record(doc, field_path, value, None, records)
