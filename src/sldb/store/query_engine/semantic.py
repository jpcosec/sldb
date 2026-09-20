from __future__ import annotations

from pathlib import Path

from sldb.store.query_engine.semantic_utils import (
    _local_semantic_docs,
    _semantic_children,
    _match_semantic_pattern,
    tag_scope,
)
from sldb.store.query_engine.where_parse import compile_where


def list_semantic(
    store_path: Path, address: str, resolve_model_ref, pythonpath: str | None = None,
) -> list[str]:
    """Lists nodes in the semantic address space (se)."""
    return SemanticEngine.list_semantic(store_path, address, resolve_model_ref, pythonpath)

def get_semantic(
    store_path: Path, address: str, resolve_model_ref, pythonpath: str | None = None,
) -> list[str]:
    """Gets documents associated with a semantic tag."""
    return SemanticEngine.get_semantic(store_path, address, resolve_model_ref, pythonpath)

def glob_semantic(
    store_path: Path, pattern: str, resolve_model_ref, pythonpath: str | None = None,
) -> list[str]:
    """Globs semantic tags."""
    return SemanticEngine.glob_semantic(store_path, pattern, resolve_model_ref, pythonpath)

def find_semantic(
    store_path: Path, address: str, where: str, resolve_model_ref, pythonpath: str | None = None,
) -> list[str]:
    """Finds documents matching a semantic scope and filter."""
    return SemanticEngine.find_semantic(store_path, address, where, resolve_model_ref, pythonpath)

class SemanticEngine:
    """Engine for processing local semantic queries."""

    @classmethod
    def list_semantic(
        cls, store_path: Path, address: str, resolve_model_ref, pythonpath: str | None = None,
    ) -> list[str]:
        """Lists nodes in the semantic address space (se)."""
        docs, _ = _local_semantic_docs(store_path, resolve_model_ref, pythonpath)
        if address == "se":
            return _semantic_children(store_path, "")
        prefix = address.removeprefix("se.")
        children = _semantic_children(store_path, prefix)
        return children if children else sorted(doc.name for doc in docs if prefix in doc.semantic_tags)

    @classmethod
    def get_semantic(
        cls, store_path: Path, address: str, resolve_model_ref, pythonpath: str | None = None,
    ) -> list[str]:
        """Gets documents associated with a semantic tag."""
        docs, _ = _local_semantic_docs(store_path, resolve_model_ref, pythonpath)
        wanted = tag_scope(store_path, address.removeprefix("se."))
        return sorted(f"st.{{{doc.model_name}}}.{doc.name}" for doc in docs if wanted & set(doc.semantic_tags))

    @classmethod
    def glob_semantic(
        cls, store_path: Path, pattern: str, resolve_model_ref, pythonpath: str | None = None,
    ) -> list[str]:
        """Globs semantic tags."""
        _, semantic_index = _local_semantic_docs(store_path, resolve_model_ref, pythonpath)
        semantic_pattern = pattern.removeprefix("se.")
        return sorted(f"se.{tag}" for tag in semantic_index.tags.keys() if _match_semantic_pattern(tag, semantic_pattern))

    @classmethod
    def find_semantic(
        cls, store_path: Path, address: str, where: str, resolve_model_ref, pythonpath: str | None = None,
    ) -> list[str]:
        """Finds documents matching a semantic scope and filter."""
        docs, _ = _local_semantic_docs(store_path, resolve_model_ref, pythonpath)
        semantic_pattern = address.removeprefix("se.")
        matching = [doc for doc in docs if cls._in_scope(store_path, semantic_pattern, doc)]
        predicate = compile_where(where)  # once per query; unparseable predicates raise
        return sorted(f"st.{{{doc.model_name}}}.{doc.name}" for doc in matching if predicate(doc, resolve_model_ref, pythonpath))

    @classmethod
    def _in_scope(cls, store_path: Path, pattern: str, doc) -> bool:
        """A glob still matches tag by tag; a plain tag names its whole subtree."""
        if "*" in pattern:
            return any(_match_semantic_pattern(tag, pattern) for tag in doc.semantic_tags)
        return bool(tag_scope(store_path, pattern) & set(doc.semantic_tags))
