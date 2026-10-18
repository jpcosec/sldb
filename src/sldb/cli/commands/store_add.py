"""`sldb stores add`: CLI adapter over `sldb.api.link_store`.

The link helpers moved to `sldb.api.stores.link_store`; they are re-exported here because
pron imports `_link_store`.
"""
from __future__ import annotations
from typing import Any
from sldb.api.stores.link_store import _check_other_exists, _check_store_linked, link_store  # noqa: F401
from sldb.api.stores.link_store import record_store_link as _link_store  # noqa: F401
from sldb.api.stores.unlink_store import unlink_store

def add_store(args: Any) -> int:
    linked = link_store(args.store, args.path, args.name, replace=getattr(args, "replace", False))
    print(f"Linked '{linked.name}' at {linked.path}")
    return 0


def remove_store(args: Any) -> int:
    removed = unlink_store(args.store, args.name)
    print(f"Removed link '{removed.name}' (was {removed.path})")
    return 0
