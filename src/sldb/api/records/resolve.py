from typing import Any
from sldb.store.query import load_runtime_documents
from sldb.core.exceptions import SLDBDocumentTargetError
from sldb.api.stores.open_store import open_store
from sldb.api.model_registry.model_reference import resolve_model_ref

def resolve_runtime_doc(store_arg: str | None, doc_ref: str, pythonpath: str | None) -> dict[str, Any]:
    location = open_store(store_arg)
    store_path, root = location.store_path, location.project_root
    docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath)
    normalized = doc_ref.strip("/")
    candidates = [doc for doc in docs if normalized in [doc.name, doc.path, f"{doc.model_name}/{doc.name}"]]
    return _build_doc_result(candidates, doc_ref, root)

def _build_doc_result(candidates, doc_ref, root):
    if not candidates: raise SLDBDocumentTargetError(f"Unknown document target: {doc_ref}")
    if len(candidates) > 1: raise SLDBDocumentTargetError(f"Ambiguous document target '{doc_ref}'. Use 'Model/DocName' or a tracked path.")
    doc = candidates[0]
    template: str | None = getattr(doc.model_type, "__template__", None)
    return {
        "store": doc.store_name, "model": doc.model_name, "name": doc.name, "path": doc.path,
        "absolute_path": str((root / doc.path).resolve()), "payload": doc.payload,
        "semantic_tags": doc.semantic_tags, "template": template,
    }
