"""Resolve a store argument (a path, a linked-store alias or nothing) to a `.sldb` directory.

Moved here from `sldb.cli.store_context`, which re-exports these names for existing importers.
"""

from __future__ import annotations

import sys
from pathlib import Path

from sldb.core.exceptions import SLDBStoreError
from sldb.store.io import load_store_index
from sldb.store.layout import project_root, store_exists
from sldb.store.resolver import ancestor_stores, find_project_store, global_store_path


def _handle_global_store(global_store: Path, mode: str, cwd: Path) -> Path:
    """Fall back to the global store in readonly mode; otherwise explain how to get a store."""
    if not global_store.exists():
        raise SLDBStoreError(f"No local .sldb store found from {cwd}. No global store exists at {global_store}. Run 'sldb stores init --path .' to create one, or pass --store PATH.")
    if mode == "readonly":
        print(f"[warning] No local .sldb store; falling back to global store at {global_store}", file=sys.stderr)
        return global_store
    raise SLDBStoreError(f"No local .sldb store found from {cwd}. A global store exists at {global_store}. Pass --store {global_store} to use it, or run 'sldb stores init --path .' to create a local store.")


def _find_default_store(mode: str) -> Path:
    """The nearest project store above the working directory, else the global store rules."""
    found = find_project_store()
    if found:
        return found
    cwd = Path.cwd().resolve()
    global_store = global_store_path().resolve()
    return _handle_global_store(global_store, mode, cwd)


def _resolve_linked_path(linked_path: Path, local_root: Path, store_arg: str) -> Path:
    """Absolute path of a linked store entry, which must exist."""
    resolved = linked_path if linked_path.is_absolute() else (local_root / linked_path)
    resolved = resolved.resolve()
    if not store_exists(resolved):
        raise SLDBStoreError(f"Linked store '{store_arg}' does not exist at {resolved}.")
    return resolved


def _get_linked_store(registry_store: Path, store_arg: str) -> Path | None:
    """The store a registry links under the alias `store_arg`, if any."""
    linked = next((entry for entry in load_store_index(registry_store).stores if entry.name == store_arg), None)
    if linked is None:
        return None
    return _resolve_linked_path(Path(linked.path), project_root(registry_store), store_arg)


def _alias_registries() -> list[Path]:
    """Stores whose links may resolve an alias: ancestors first, the global store last."""
    global_store = global_store_path().resolve()
    registries = [store for store in ancestor_stores() if store != global_store]
    if store_exists(global_store):
        registries.append(global_store)
    return registries


def _resolve_store_arg(store_arg: str) -> Path:
    """A store path when one exists there, else an alias linked by an ancestor or global store."""
    candidate = Path(store_arg).resolve()
    if store_exists(candidate):
        return candidate
    for registry_store in _alias_registries():
        linked = _get_linked_store(registry_store, store_arg)
        if linked is not None:
            return linked
    return candidate
