from __future__ import annotations

from pathlib import Path

from sldb.store.query_engine.semantic_utils import (
    _local_semantic_docs,
    _semantic_children,
    _match_semantic_pattern,
)
from sldb.store.query_engine.filter import _where_matches


def list_semantic(
    store_path: Path, address: str, resolve_model_ref, pythonpath: str | None = None,
) -> list[str]:
    """Lists nodes in the semantic address space (se)."""
    docs, semantic_index = _local_semantic_docs(store_path, resolve_model_ref, pythonpath)
    tags = sorted(semantic_index.tags.keys())
    if address == "se":
        return _semantic_children(tags, "")
    prefix = address.removeprefix("se.")
    children = _semantic_children(tags, prefix)
    return children if children else sorted(doc.name for doc in docs if prefix in doc.semantic_tags)


def get_semantic(
    store_path: Path, address: str, resolve_model_ref, pythonpath: str | None = None,
) -> list[str]:
    """Gets documents associated with a semantic tag."""
    docs, _ = _local_semantic_docs(store_path, resolve_model_ref, pythonpath)
    tag = address.removeprefix("se.")
    return sorted(f"st.{{{doc.model_name}}}.{doc.name}" for doc in docs if tag in doc.semantic_tags)


def glob_semantic(
    store_path: Path, pattern: str, resolve_model_ref, pythonpath: str | None = None,
) -> list[str]:
    """Globs semantic tags."""
    _, semantic_index = _local_semantic_docs(store_path, resolve_model_ref, pythonpath)
    semantic_pattern = pattern.removeprefix("se.")
    return sorted(f"se.{tag}" for tag in semantic_index.tags.keys() if _match_semantic_pattern(tag, semantic_pattern))


def find_semantic(
    store_path: Path, address: str, where: str, resolve_model_ref, pythonpath: str | None = None,
) -> list[str]:
    """Finds documents matching a semantic scope and filter."""
    docs, _ = _local_semantic_docs(store_path, resolve_model_ref, pythonpath)
    semantic_pattern = address.removeprefix("se.")
    matching = [doc for doc in docs if any(_match_semantic_pattern(tag, semantic_pattern) for tag in doc.semantic_tags)]
    return sorted(f"st.{{{doc.model_name}}}.{doc.name}" for doc in matching if _where_matches(doc, where, resolve_model_ref, pythonpath))
