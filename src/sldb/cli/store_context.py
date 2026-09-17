"""Compatibility bridge: store resolution now lives in `sldb.api.stores`.

`get_store_context` keeps its tuple-returning signature for existing importers (the sldb CLI
commands, deskops, kgdb, pron); new code should call `sldb.api.open_store`. The private
helpers are re-exported because `sldb.cli.selfdoc_context` imports them.
"""
from __future__ import annotations
from pathlib import Path
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_discovery import (  # noqa: F401 - re-exported for existing importers
    _alias_registries,
    _find_default_store,
    _get_linked_store,
    _handle_global_store,
    _resolve_linked_path,
    _resolve_store_arg,
)

def get_store_context(store_arg: str | None, mode: str = "default") -> tuple[Path, Path]:
    """Resolves once per Store/World opened (pron: once per session) or per sldb CLI command
    — the natural "start of an operation" a fresh document-leaf sweep belongs to (PLAN 15
    capa 6: `new_operation` schedules that sweep for the next `runtime_cache.signature`)."""
    location = open_store(store_arg, mode)
    return location.store_path, location.project_root
