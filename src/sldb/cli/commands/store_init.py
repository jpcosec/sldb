"""`sldb stores init`: CLI adapter over `sldb.api.init_store`."""
from __future__ import annotations
from pathlib import Path
from typing import Any
from sldb.api.stores.init_store import init_store as create_store
from sldb.store.layout import store_exists

def init_store(args: Any) -> int:
    root = Path(args.path).resolve()
    if store_exists(root / ".sldb") and not args.force:
        print(f"Store already exists at {root / '.sldb'}. Use --force to reinitialize.")
        return 0
    created = create_store(root, args.force)
    print(f"Initialized store at {created.store_path}")
    return 0
