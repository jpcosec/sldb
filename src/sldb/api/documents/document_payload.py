"""One tracked document's runtime record and payload addressing, api-side.

``runtime_document`` narrows ``load_runtime_documents`` to one document by name,
path or ``Model/name``, optionally behind ``alias:`` for a linked store; it is the one
resolver the CLI's ``resolve_runtime_doc`` and the serve routes share. ``leaf_paths`` names every
addressable field of a payload with the dotted paths ``deep_get`` reads.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.stores.doc_ref import LOCAL, matches_doc_ref, qualifier, split_doc_ref
from sldb.api.stores.store_links import find_link
from sldb.core.exceptions import SLDBDocumentTargetError
from sldb.store.query import load_runtime_documents


def runtime_document(store_path: Path, pythonpath: str | None, doc_ref: str) -> Any:
    """The RuntimeDocument of one doc; unknown or ambiguous refs raise SLDBDocumentTargetError.

    `alias:ref` reads only the store directly linked under `alias` (see `sldb.api.stores.doc_ref`);
    a bare ref reads only the local store.
    """
    alias, ref = split_doc_ref(store_path, doc_ref)
    docs = _scoped_documents(store_path, alias, pythonpath)
    candidates = [doc for doc in docs if matches_doc_ref(ref, doc.name, doc.path, doc.model_name)]
    if not candidates:
        raise SLDBDocumentTargetError(_unknown_target(doc_ref, alias))
    if len(candidates) > 1:
        raise SLDBDocumentTargetError(f"Ambiguous document target '{doc_ref}'. Use 'Model/DocName' or a tracked path.")
    return candidates[0]


def _scoped_documents(store_path: Path, alias: str | None, pythonpath: str | None) -> list[Any]:
    if alias is None:
        return load_runtime_documents(store_path, resolve_model_ref, pythonpath)
    link = find_link(store_path, alias)
    if link["status"] != "ok":
        raise SLDBDocumentTargetError(f"Linked store '{alias}' is {link['status']}: {link['resolved']}")
    return load_runtime_documents(Path(link["resolved"]), resolve_model_ref, pythonpath, store_name=alias)


def _unknown_target(doc_ref: str, alias: str | None) -> str:
    prefix = qualifier(doc_ref)
    hint = f" (no linked store named '{prefix}')" if alias is None and prefix not in (None, LOCAL) else ""
    return f"Unknown document target: {doc_ref}{hint}"


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