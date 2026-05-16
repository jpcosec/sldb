from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from sldb.store.io import load_store_index


def _model_scope_docs(
    store_path: Path,
    scope: str,
    recursive: bool,
    resolve_model_ref,
    pythonpath: str | None = None,
) -> list[Any]:
    from sldb.store.query import load_runtime_documents
    docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath)
    if scope == "*":
        return docs
    base_doc = next((doc for doc in docs if doc.model_name == scope), None)
    if base_doc is None:
        return []
    if not recursive:
        return [doc for doc in docs if doc.model_name == scope]
    return [doc for doc in docs if issubclass(doc.model_type, base_doc.model_type)]


def list_structural(
    store_path: Path, address: str, resolve_model_ref, pythonpath: str | None = None
) -> list[str]:
    """Lists structural nodes (st.{Model})."""
    if address == "st":
        store_index = load_store_index(store_path)
        return sorted(f"st.{{{entry.name}}}" for entry in store_index.models)

    match = re.fullmatch(r"st\.\{([^{}+]+)(\+)?\}(?:\.([^.]+))?", address)
    if not match:
        return []
    model_name, recursive_flag, doc_name = match.groups()
    docs = _model_scope_docs(store_path, model_name, bool(recursive_flag), resolve_model_ref, pythonpath)
    if doc_name is None:
        return sorted(doc.name for doc in docs)
    target = next((doc for doc in docs if doc.name == doc_name), None)
    if not target:
        return []

    results = []
    for key in sorted(target.payload.keys()):
        field = getattr(target.model_type, "model_fields", {}).get(key)
        description = field.description if field and field.description else ""
        results.append(f"{key}: {description}" if description else key)
    return results


def get_structural(
    store_path: Path, address: str, resolve_model_ref, pythonpath: str | None = None
) -> Any:
    """Gets value from a structural address."""
    match = re.fullmatch(r"st\.\{([^{}+]+)(\+)?\}\.([^.]+)(?:\.(.+))?", address)
    if not match:
        return None
    model_name, recursive_flag, doc_name, field_name = match.groups()
    docs = _model_scope_docs(store_path, model_name, bool(recursive_flag), resolve_model_ref, pythonpath)
    target = next((doc for doc in docs if doc.name == doc_name), None)
    if target is None:
        return None
    if field_name is None:
        return target.payload
    value: Any = target.payload
    for part in field_name.split("."):
        if isinstance(value, dict) and part in value:
            value = value[part]
        else:
            return None
    return value
