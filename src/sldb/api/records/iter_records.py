import logging
from sldb.store.io import load_store_index
from sldb.store.query import load_runtime_documents
from sldb.api.stores.open_store import open_store
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.records.search_record import SearchRecord
from .iter_records_helpers import _load_model_sections, _build_store_records, _process_docs

logger = logging.getLogger(__name__)

def iter_search_records(store_arg: str | None, pythonpath: str | None, include_linked: bool = False, rebuild: bool = False) -> list[SearchRecord]:
    location = open_store(store_arg)
    store_path, root = location.store_path, location.project_root
    store_index = load_store_index(store_path)
    runtime_docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath, include_linked=include_linked)
    model_sections = _load_model_sections(store_index, root, rebuild)
    records = _build_store_records(store_path, root, store_index)
    _process_docs(runtime_docs, store_index, model_sections, records)
    return records
