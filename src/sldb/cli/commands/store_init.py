"""`sldb stores init`: CLI adapter over `sldb.api.init_store`."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import sys
from sldb.api.stores.init_store import StoreInitError, init_store as create_store
from sldb.store.layout import store_exists
from sldb.api.stores.branch_stores import branches_with_store

def init_store(args: Any) -> int:
    root = Path(args.path).resolve()
    if store_exists(root / ".sldb") and not args.force:
        print(f"Store already exists at {root / '.sldb'}. Use --force to reinitialize.")
        return 0
    _alert_other_branches(root)
    return _create(root, args.force)

def _alert_other_branches(root: Path) -> None:
    """One store per repository: a store another branch already has meets this one only in a merge."""
    for branch in branches_with_store(root):
        print(f"alert: branch '{branch}' already has a store at .sldb/; merge that branch instead of creating a second store (one store per repository)", file=sys.stderr)

def _create(root: Path, force: bool) -> int:
    """0 created; 2 the place refused it (permissions); 1 failed half-way. Nothing is left behind."""
    try:
        created = create_store(root, force)
    except StoreInitError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2 if exc.precondition else 1
    print(f"Initialized store at {created.store_path}")
    return 0
