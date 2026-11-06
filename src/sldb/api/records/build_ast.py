from typing import Any
from sldb.store.io import load_store_index, load_models_index, load_documents_index
from sldb.store.query import load_runtime_documents
from sldb.api.stores.open_store import open_store
from sldb.api.model_registry.model_reference import resolve_model_ref
from .utils import _annotation_name
from sldb.core.exceptions import SLDBModelError

def build_store_ast(store_arg: str | None, pythonpath: str | None, include_linked: bool = False) -> dict[str, Any]:
    location = open_store(store_arg)
    store_path, root = location.store_path, location.project_root
    store_index = load_store_index(store_path)
    linked = [{"name": entry.name, "path": entry.path} for entry in sorted(store_index.stores, key=lambda item: item.name)]
    models = _build_models_ast(store_index, root, pythonpath)
    ast: dict[str, Any] = {"store": {"path": str(store_path), "root": str(root), "linked_stores": linked, "models": models}}
    if include_linked: _add_linked_documents(ast, store_path, pythonpath)
    return ast

def _build_models_ast(store_index, root, pythonpath) -> list[dict[str, Any]]:
    models: list[dict[str, Any]] = []
    for entry in sorted(store_index.models, key=lambda item: item.name):
        _process_model_entry(entry, root, pythonpath, models)
    return models

def _process_model_entry(entry, root, pythonpath, models):
    models_index = load_models_index(root / entry.models_index)
    docs_index = load_documents_index(root / models_index.documents_index)
    fields, meta, problem = _fields_of(entry, root, pythonpath)
    documents = [{"name": doc.name, "path": doc.path, "semantic_tags": list(doc.semantic_tags)} for doc in sorted(docs_index.documents, key=lambda item: item.name)]
    _append_model_ast(models, entry, models_index, fields, documents, meta)
    if problem:
        models[-1].update({"resolved": False, "error": problem})  # only then: a healthy model's shape is describe_model's

def _fields_of(entry, root, pythonpath) -> tuple[list[dict[str, Any]], dict[str, Any], str | None]:
    """The model's fields, or none and why: one model that does not import (its package is not
    installed here) used to abort the whole store's AST, so `models show` of any other failed."""
    try:
        model_type = resolve_model_ref(entry.model_ref, pythonpath)
    except SLDBModelError as exc:
        return [], {}, str(exc)
    fields = [{"name": fname, "annotation": _annotation_name(f.annotation), "description": f.description or ""} for fname, f in model_type.model_fields.items()]
    has_draft = False
    draft_p = None
    try:
        from sldb.api.model_drafts.source_location import locate_model_source
        src = locate_model_source(root / ".sldb", entry.name, pythonpath)
        if src.draft_path.exists():
            has_draft = True
            draft_p = str(src.draft_path)
    except Exception:
        pass
    meta = {
        "containment": dict(getattr(model_type, "__containment__", {}) or {}),
        "references": list(getattr(model_type, "__references__", []) or []),
        "compositions": dict(getattr(model_type, "__compositions__", {}) or {}),
        "semantics_map": dict(getattr(model_type, "__semantics__", {}) or {}),
        "authority": str(getattr(model_type, "__authority__", "generated")),
        "template": str(getattr(model_type, "__template__", "")),
        "has_draft": has_draft,
        "draft_path": draft_p,
    }
    return fields, meta, None

def _append_model_ast(models, entry, models_index, fields, documents, meta):
    models.append({
        "name": entry.name, "model_ref": entry.model_ref, "path": entry.path,
        "version": getattr(models_index, "version", 1), "canonical": getattr(models_index, "canonical", False),
        "family": getattr(models_index, "family", None), "semantics": list(getattr(models_index, "semantics", [])),
        "base_models": list(getattr(models_index, "base_models", [])), "fields": fields, "documents": documents,
        **meta,
    })

def _add_linked_documents(ast, store_path, pythonpath):
    ast["linked_documents"] = [
        {"store": doc.store_name, "model": doc.model_name, "doc": doc.name, "path": doc.path, "semantic_tags": doc.semantic_tags}
        for doc in load_runtime_documents(store_path, resolve_model_ref, pythonpath, include_linked=True)
        if doc.store_name != "local"
    ]
