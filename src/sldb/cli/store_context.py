from __future__ import annotations
import sys
from pathlib import Path
from sldb.store.resolver import global_store_path, find_local_store
from sldb.core.exceptions import SLDBStoreError
from sldb.store.layout import project_root, store_exists
from sldb.store.migration import migrate_store_layout
from sldb.store.io import load_store_index
from sldb.store.runtime_cache import new_operation
from sldb.store.documents_hash import new_operation as new_documents_hash_operation

def _handle_global_store(global_store: Path, mode: str, cwd: Path) -> Path:
    if not global_store.exists():
        raise SLDBStoreError(f"No local .sldb store found from {cwd}. No global store exists at {global_store}. Run 'sldb stores init --path .' to create one, or pass --store PATH.")
    if mode == "readonly":
        print(f"[warning] No local .sldb store; falling back to global store at {global_store}", file=sys.stderr)
        return global_store
    raise SLDBStoreError(f"No local .sldb store found from {cwd}. A global store exists at {global_store}. Pass --store {global_store} to use it, or run 'sldb stores init --path .' to create a local store.")

def _find_default_store(mode: str) -> Path:
    found = find_local_store()
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

def _get_linked_store(local_store: Path, store_arg: str, candidate: Path) -> Path:
    local_root = project_root(local_store)
    store_index = load_store_index(local_store)
    linked = next((entry for entry in store_index.stores if entry.name == store_arg), None)
    if linked is None:
        return candidate
    return _resolve_linked_path(Path(linked.path), local_root, store_arg)

def _resolve_store_arg(store_arg: str) -> Path:
    candidate = Path(store_arg).resolve()
    if store_exists(candidate):
        return candidate
    local_store = find_local_store()
    if local_store is None:
        return candidate
    return _get_linked_store(local_store, store_arg, candidate)

def get_store_context(store_arg: str | None, mode: str = "default") -> tuple[Path, Path]:
    """Resolves once per Store/World opened (pron: once per session) or per sldb CLI command
    — the natural "start of an operation" a fresh document-leaf sweep belongs to (PLAN 15
    capa 6: `new_operation` schedules that sweep for the next `runtime_cache.signature`)."""
    sp = _resolve_store_arg(store_arg) if store_arg else _find_default_store(mode)
    root = project_root(sp)
    if store_exists(sp):
        migrate_store_layout(sp, root)
    new_operation(sp)
    new_documents_hash_operation(sp)
    return sp, root
