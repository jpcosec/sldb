"""One tracked document's runtime record and payload addressing, api-side.

``runtime_document`` narrows ``load_runtime_documents`` to one document by name,
path or ``Model/name`` — the same narrowing the CLI's ``resolve_runtime_doc``
does — so the serve routes speak only to ``sldb.api``. ``leaf_paths`` names every
addressable field of a payload with the dotted paths ``deep_get`` reads.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.store.query import load_runtime_documents


def runtime_document(store_path: Path, pythonpath: str | None, doc_ref: str) -> Any:
    """The RuntimeDocument of one doc; unknown or ambiguous refs raise ValueError."""
    docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath)
    normalized = doc_ref.strip("/")
    candidates = [doc for doc in docs if normalized in (doc.name, doc.path, f"{doc.model_name}/{doc.name}")]
    if not candidates:
        raise ValueError(f"Unknown document target: {doc_ref}")
    if len(candidates) > 1:
        raise ValueError(f"Ambiguous document target '{doc_ref}'. Use 'Model/DocName' or a tracked path.")
    return candidates[0]


def leaf_paths(payload: dict[str, Any]) -> list[str]:
    """Every leaf address (dotted path) of a payload, shallow lists by index."""
    paths: list[str] = []
    _walk(payload, "", paths)
    return [path for path in paths if path]


def _walk(value: Any, prefix: str, paths: list[str]) -> None:
    if isinstance(value, dict):
        _walk_mapping(value, prefix, paths)
        return
    if isinstance(value, list):
        _walk_sequence(value, prefix, paths)
        return
    paths.append(prefix)


def _walk_mapping(value: dict[str, Any], prefix: str, paths: list[str]) -> None:
    if not value and prefix:
        paths.append(prefix)
        return
    for key, item in value.items():
        _walk(item, f"{prefix}.{key}" if prefix else key, paths)


def _walk_sequence(value: list[Any], prefix: str, paths: list[str]) -> None:
    if not value and prefix:
        paths.append(prefix)
        return
    for index, item in enumerate(value):
        _walk(item, f"{prefix}.{index}", paths)