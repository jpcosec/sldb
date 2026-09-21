"""Legacy single-document POST /save: unchanged behavior, now under the save lock."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.cli.commands.fields_save import save_payload
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.query import load_runtime_documents


def save_single(request: dict[str, Any], store_path: Path, pythonpath: str) -> tuple[dict[str, Any], int]:
    doc_name = request.get("doc")
    payload = request.get("payload")
    ensure_save_request(doc_name, payload)
    runtime_doc = find_runtime_document(store_path, pythonpath, doc_name)
    if runtime_doc is None:
        return {"ok": False, "error": f"Unknown doc: {doc_name}"}, 404
    save_payload(runtime_doc, payload, str(store_path), pythonpath)
    return {"ok": True, "doc": doc_name}, 200


def ensure_save_request(doc_name: Any, payload: Any) -> None:
    if not isinstance(doc_name, str):
        raise ValueError("Expected 'doc' to be a string")
    if not isinstance(payload, dict):
        raise ValueError("Expected 'payload' to be an object")


def find_runtime_document(store_path: Path, pythonpath: str, doc_name: str) -> Any:
    docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath)
    return next((doc for doc in docs if doc.name == doc_name), None)