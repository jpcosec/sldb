from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from sldb.store.layout import project_root
from sldb.store.io import load_semantic_index
from sldb.store.query import load_runtime_documents
from sldb.store.query_engine.models import RuntimeDocument


def _match_semantic_pattern(tag: str, pattern: str) -> bool:
    """Matches a semantic tag against a glob-like pattern (** or *)."""
    escaped = re.escape(pattern)
    escaped = escaped.replace(re.escape("**"), ".*")
    escaped = escaped.replace(re.escape("*"), "[^.]+")
    return re.fullmatch(escaped, tag) is not None


def _semantic_children(tags: list[str], prefix: str) -> list[str]:
    """Retrieves child semantic nodes for a given prefix."""
    children = set()
    prefix_dot = f"{prefix}." if prefix else ""
    for tag in tags:
        if not tag.startswith(prefix_dot):
            continue
        remainder = tag[len(prefix_dot) :]
        if not remainder or "." not in remainder:
            continue
        children.add(remainder.split(".", 1)[0])
    return sorted(children)


def _local_semantic_docs(
    store_path: Path, resolve_model_ref, pythonpath: str | None = None
) -> tuple[list[RuntimeDocument], Any]:
    """Loads docs and the semantic index, rebuilding if necessary."""
    docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath)
    semantic_index = load_semantic_index(store_path)
    if not semantic_index.documents:
        from sldb.store.semantic import rebuild_semantic_indexes

        rebuild_semantic_indexes(
            store_path,
            project_root(store_path),
            resolve_model_ref,
            pythonpath,
        )
        semantic_index = load_semantic_index(store_path)
    return docs, semantic_index
