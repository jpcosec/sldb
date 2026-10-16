from typing import Any
from sldb.api.documents.document_payload import runtime_document
from sldb.api.stores.open_store import open_store
from sldb.store.layout import project_root

def resolve_runtime_doc(store_arg: str | None, doc_ref: str, pythonpath: str | None) -> dict[str, Any]:
    """One document as a dict, by name, path, `Model/name` or `alias:ref` (see `runtime_document`)."""
    doc = runtime_document(open_store(store_arg).store_path, pythonpath, doc_ref)
    return _build_doc_result(doc)

def _build_doc_result(doc):
    template: str | None = getattr(doc.model_type, "__template__", None)
    return {
        "store": doc.store_name, "model": doc.model_name, "name": doc.name, "path": doc.path,
        "absolute_path": str((project_root(doc.store_path) / doc.path).resolve()), "payload": doc.payload,
        "semantic_tags": doc.semantic_tags, "template": template,
    }
