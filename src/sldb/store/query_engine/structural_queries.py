from __future__ import annotations

import fnmatch
import re
from pathlib import Path

from sldb.store.query_engine.structural import _model_scope_docs
from sldb.store.query_engine.filter import _where_matches


def glob_structural(
    store_path: Path, pattern: str, resolve_model_ref, pythonpath: str | None = None
) -> list[str]:
    """Matches structural addresses against a glob pattern."""
    match = re.fullmatch(r"st\.\{([^{}+]+)(\+)?\}\.([^.]+)(?:\.(.+))?", pattern)
    if not match:
        return []
    model_name, recursive_flag, doc_pattern, field_pattern = match.groups()
    docs = _model_scope_docs(store_path, model_name, bool(recursive_flag), resolve_model_ref, pythonpath)
    base_scope = f"st.{{{model_name}{'+' if recursive_flag else ''}}}"
    results: list[str] = []
    for doc in docs:
        if not fnmatch.fnmatch(doc.name, doc_pattern):
            continue
        if field_pattern is None:
            results.append(f"{base_scope}.{doc.name}")
            continue
        for field_name in sorted(doc.payload.keys()):
            if fnmatch.fnmatch(field_name, field_pattern):
                results.append(f"{base_scope}.{doc.name}.{field_name}")
    return sorted(results)


def find_structural(
    store_path: Path, address: str, where: str, resolve_model_ref, pythonpath: str | None = None,
) -> list[str]:
    """Finds documents matching a structural scope and filter."""
    match = re.fullmatch(r"st\.\{([^{}+]+)(\+)?\}", address)
    if not match:
        return []
    model_name, recursive_flag = match.groups()
    docs = _model_scope_docs(store_path, model_name, bool(recursive_flag), resolve_model_ref, pythonpath)
    base_scope = f"st.{{{model_name}{'+' if recursive_flag else ''}}}"
    return sorted(
        f"{base_scope}.{doc.name}"
        for doc in docs
        if _where_matches(doc, where, resolve_model_ref, pythonpath)
    )
