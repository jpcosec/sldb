from __future__ import annotations

import fnmatch
import re
from pathlib import Path

from sldb.store.query_engine.structural import _model_scope_docs
from sldb.store.query_engine.filter import _where_matches
from sldb.store.query_engine.store_prefix import split_store, with_store


def glob_structural(
    store_path: Path, pattern: str, resolve_model_ref, pythonpath: str | None = None
) -> list[str]:
    """Matches structural addresses against a glob pattern."""
    return StructuralQueryEngine.glob_structural(store_path, pattern, resolve_model_ref, pythonpath)

def find_structural(
    store_path: Path, address: str, where: str, resolve_model_ref, pythonpath: str | None = None,
) -> list[str]:
    """Finds documents matching a structural scope and filter."""
    return StructuralQueryEngine.find_structural(store_path, address, where, resolve_model_ref, pythonpath)

class StructuralQueryEngine:
    """Engine for processing glob and find queries on structural nodes."""

    @classmethod
    def glob_structural(
        cls, store_path: Path, pattern: str, resolve_model_ref, pythonpath: str | None = None
    ) -> list[str]:
        """Matches structural addresses against a glob pattern."""
        store, pattern = split_store(pattern)
        match = re.fullmatch(r"st\.\{([^{}+]+)(\+)?\}\.([^.]+)(?:\.(.+))?", pattern)
        if not match:
            return []
        model_name, recursive_flag, doc_pattern, field_pattern = match.groups()
        docs = _model_scope_docs(store_path, model_name, bool(recursive_flag), resolve_model_ref, pythonpath, store)
        base_scope = with_store(store, f"st.{{{model_name}{'+' if recursive_flag else ''}}}")
        return cls._glob_docs(docs, doc_pattern, field_pattern, base_scope)

    @classmethod
    def _glob_docs(cls, docs, doc_pattern: str, field_pattern: str | None, base_scope: str) -> list[str]:
        results: list[str] = []
        for doc in docs:
            if not fnmatch.fnmatch(doc.name, doc_pattern):
                continue
            if field_pattern is None:
                results.append(f"{base_scope}.{doc.name}")
                continue
            cls._glob_fields(doc, field_pattern, base_scope, results)
        return sorted(results)

    @classmethod
    def _glob_fields(cls, doc, field_pattern: str, base_scope: str, results: list[str]) -> None:
        for field_name in sorted(doc.payload.keys()):
            if fnmatch.fnmatch(field_name, field_pattern):
                results.append(f"{base_scope}.{doc.name}.{field_name}")

    @classmethod
    def find_structural(
        cls, store_path: Path, address: str, where: str, resolve_model_ref, pythonpath: str | None = None,
    ) -> list[str]:
        """Finds documents matching a structural scope and filter."""
        store, address = split_store(address)
        match = re.fullmatch(r"st\.\{([^{}+]+)(\+)?\}", address)
        if not match:
            return []
        return cls._find_docs(match, store_path, where, resolve_model_ref, pythonpath, store)

    @classmethod
    def _find_docs(cls, match, store_path: Path, where: str, resolve_model_ref, pythonpath: str | None, store: str | None = None) -> list[str]:
        model_name, recursive_flag = match.groups()
        docs = _model_scope_docs(store_path, model_name, bool(recursive_flag), resolve_model_ref, pythonpath, store)
        base_scope = with_store(store, f"st.{{{model_name}{'+' if recursive_flag else ''}}}")
        return sorted(
            f"{base_scope}.{doc.name}"
            for doc in docs
            if _where_matches(doc, where, resolve_model_ref, pythonpath)
        )
