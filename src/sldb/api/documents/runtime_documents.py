"""Bulk runtime load through sldb.api: every tracked document, payload and both hashes.

``sldb r…``/serve consumers used to import ``sldb.store.query.load_runtime_documents``
directly; this wrapper supplies the model resolver the store function takes as a parameter,
so a consumer names only a store path, an optional pythonpath and whether to follow links.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.store.query import load_runtime_documents as _load_runtime_documents


def load_runtime_documents(store_path: Path, pythonpath: str | None = None, include_linked: bool = False) -> list[Any]:
    """Every runtime document of `store_path`, extracted, with its two index hashes."""
    return _load_runtime_documents(store_path, resolve_model_ref, pythonpath, include_linked=include_linked)
