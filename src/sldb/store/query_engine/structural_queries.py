from __future__ import annotations

import fnmatch
import re
from pathlib import Path

from sldb.store.graph.language.predicate_documents import document_matcher
from sldb.store.query_engine.document_selection import select_rows
from sldb.store.query_engine.store_prefix import scoped_docs, split_store, with_store


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
    """Engine for processing glob and find queries on structural nodes. The documents of a
    scope are chosen by `document_selection` (exact model or family); the name pattern, the
    expansion to fields and `find`'s `where` (on each document's own payload, as always) stay
    here, as does the address form of the results."""

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
        docs = cls._chosen_docs(store_path, model_name, bool(recursive_flag), resolve_model_ref, pythonpath, store)
        base_scope = with_store(store, f"st.{{{model_name}{'+' if recursive_flag else ''}}}")
        return cls._glob_docs(docs, doc_pattern, field_pattern, base_scope)

    @classmethod
    def _chosen_docs(cls, store_path: Path, model_name: str, recursive: bool, resolve_model_ref, pythonpath: str | None, store: str | None) -> list:
        """The runtime documents of scope `{Model}` (exact) or `{Model+}` (the family), of the
        local store or of the linked store `store`, that `document_selection` keeps."""
        rows = select_rows(store_path, model=None if model_name == "*" else model_name, include_linked=store is not None)
        chosen = {r["export_id"] for r in rows if recursive or model_name == "*" or r["model"] == model_name}
        docs = scoped_docs(store_path, store, resolve_model_ref, pythonpath)
        return [doc for doc in docs if with_store(store, f"{doc.model_name}:{doc.name}") in chosen]

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
        docs = cls._chosen_docs(store_path, model_name, bool(recursive_flag), resolve_model_ref, pythonpath, store)
        base_scope = with_store(store, f"st.{{{model_name}{'+' if recursive_flag else ''}}}")
        predicate = document_matcher(where)  # once per query; unparseable predicates raise
        return sorted(f"{base_scope}.{doc.name}" for doc in docs if predicate(doc, resolve_model_ref, pythonpath))
