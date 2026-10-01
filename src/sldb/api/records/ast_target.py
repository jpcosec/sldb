from pathlib import Path
from typing import Any
from .build_ast import build_store_ast
from .resolve import resolve_runtime_doc
from .build_ir import build_document_ir
from .extract import extract_sections
from .fields import query_field_records
from sldb.core.exceptions import SLDBDocumentTargetError

def ast_for_target(store_arg: str | None, pythonpath: str | None, target: str) -> dict[str, Any]:
    graph = build_store_ast(store_arg, pythonpath)
    store = graph["store"]
    target = (target or "store").strip("/")
    if target in {"", "store", "stores"}: return graph
    if target.startswith("models/"): return _ast_for_model(target, store)
    if target.startswith("docs/"): return _ast_for_doc(target, store_arg, pythonpath)
    if target.startswith("fields/"): return _ast_for_field(target, store_arg, pythonpath)
    raise SLDBDocumentTargetError(f"Unknown ast target: {target}")

def _ast_for_model(target, store):
    model_name = target.split("/", 1)[1]
    model = next((item for item in store["models"] if item["name"] == model_name), None)
    if model is None: raise SLDBDocumentTargetError(f"Unknown model target: {target}")
    return {"model": model}

def _ast_for_doc(target, store_arg, pythonpath):
    doc_ref = target.split("/", 1)[1]
    runtime_doc = resolve_runtime_doc(store_arg, doc_ref, pythonpath)
    return _build_doc_ast(runtime_doc)

def _build_doc_ast(runtime_doc):
    markdown = Path(runtime_doc["absolute_path"]).read_text(encoding="utf-8")
    ir = build_document_ir(runtime_doc, markdown, template=runtime_doc.get("template"))
    return {
        "document": {
            "store": runtime_doc["store"], "model": runtime_doc["model"], "name": runtime_doc["name"],
            "path": runtime_doc["path"], "semantic_tags": runtime_doc["semantic_tags"], "payload": runtime_doc["payload"],
            "sections": [section.__dict__ for section in extract_sections(markdown)], "ir": ir.model_dump(mode="json"),
        }
    }

def _ast_for_field(target, store_arg, pythonpath):
    field_ref = target.split("/", 1)[1]
    docs = query_field_records(store_arg, pythonpath, field_ref, include_linked=False)
    return {"field": {"target": field_ref, "matches": docs}}
