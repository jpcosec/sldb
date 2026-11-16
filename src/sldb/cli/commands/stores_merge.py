"""CLI adapters of `sldb stores rebuild-index` and `sldb stores merge-driver`."""
from __future__ import annotations

from typing import Any

from sldb.api.stores.merge_driver import merge_driver
from sldb.api.stores.merge_driver_install import install_merge_driver
from sldb.api.stores.rebuild_index import locate_store, rebuild_index


def rebuild_index_command(args: Any) -> int:
    report = rebuild_index(args.store)
    for path in report["repaired"]:
        print(f"repaired {path}")
    print(f"rebuilt {len(report['models'])} model indexes and the store index")
    return 0


def merge_driver_command(args: Any) -> int:
    if args.install:
        done = install_merge_driver(locate_store(args.store))
        print(f"merge driver installed: {len(done['attributes'])} .gitattributes lines added, {len(done['config'])} git config keys set")
        return 0
    if len(args.files) != 4:
        print("usage: sldb stores merge-driver %O %A %B %P  (or --install)")
        return 2
    return merge_driver(*args.files)
