from __future__ import annotations
import sys
from pathlib import Path
from sldb.store.resolver import ancestor_stores, global_store_path, find_project_store
from sldb.core.exceptions import SLDBStoreError
from sldb.store.layout import project_root, store_exists
from sldb.store.migration import migrate_store_layout
from sldb.store.io import load_store_index

def _handle_global_store(global_store: Path, mode: str, cwd: Path) -> Path:
    if not global_store.exists():
        raise SLDBStoreError(f"No local .sldb store found from {cwd}. No global store exists at {global_store}. Run 'sldb stores init --path .' to create one, or pass --store PATH.")
    if mode == "readonly":
        print(f"[warning] No local .sldb store; falling back to global store at {global_store}", file=sys.stderr)
        return global_store
    raise SLDBStoreError(f"No local .sldb store found from {cwd}. A global store exists at {global_store}. Pass --store {global_store} to use it, or run 'sldb stores init --path .' to create a local store.")

def _find_default_store(mode: str) -> Path:
    found = find_project_store()
    if found:
        return found
    cwd = Path.cwd().resolve()
    global_store = global_store_path().resolve()
    return _handle_global_store(global_store, mode, cwd)

def _resolve_linked_path(linked_path: Path, local_root: Path, store_arg: str) -> Path:
    resolved = linked_path if linked_path.is_absolute() else (local_root / linked_path)
    resolved = resolved.resolve()
    if not store_exists(resolved):
        raise SLDBStoreError(f"Linked store '{store_arg}' does not exist at {resolved}.")
    return resolved

def _get_linked_store(registry_store: Path, store_arg: str) -> Path | None:
    linked = next((entry for entry in load_store_index(registry_store).stores if entry.name == store_arg), None)
    if linked is None:
        return None
    return _resolve_linked_path(Path(linked.path), project_root(registry_store), store_arg)


def _alias_registries() -> list[Path]:
    global_store = global_store_path().resolve()
    registries = [store for store in ancestor_stores() if store != global_store]
    if store_exists(global_store):
        registries.append(global_store)
    return registries

def _resolve_store_arg(store_arg: str) -> Path:
    candidate = Path(store_arg).resolve()
    if store_exists(candidate):
        return candidate
    for registry_store in _alias_registries():
        linked = _get_linked_store(registry_store, store_arg)
        if linked is not None:
            return linked
    return candidate

def get_store_context(store_arg: str | None, mode: str = "default") -> tuple[Path, Path]:
    sp = _resolve_store_arg(store_arg) if store_arg else _find_default_store(mode)
    root = project_root(sp)
    if store_exists(sp):
        migrate_store_layout(sp, root)
    return sp, root
