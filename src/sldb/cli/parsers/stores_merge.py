"""`sldb stores rebuild-index` and `sldb stores merge-driver`: merging two branches that touched `.sldb/`."""
from __future__ import annotations

REBUILD_HELP = ("Regenerate .sldb/core/store_index.yaml and .sldb/core/models/*.yaml from the document shards and "
                "each model's contract, repairing conflict markers git left in them. Run it after merging or "
                "rebasing branches that touched .sldb/, or when a command says a derived index could not be merged.")
DRIVER_HELP = ("Git merge driver for a store: derived indexes keep this branch's version (then run "
               "`sldb stores rebuild-index`), .sldb/store.yaml joins both branches' include rules, any other file "
               "is a normal conflict. Install it once per clone with --install.")


def add_merge_parsers(s) -> None:
    r = s.add_parser("rebuild-index", help="Regenerate the derived store indexes from the shards (after a merge).", description=REBUILD_HELP)
    r.add_argument("--store", help="Store path")
    d = s.add_parser("merge-driver", help="Git merge driver for .sldb/ files; --install registers it in this clone.", description=DRIVER_HELP)
    d.add_argument("files", nargs="*", metavar="%O %A %B %P", help="Base, current (result), other and merged path, as git passes them")
    d.add_argument("--install", action="store_true", help="Write .gitattributes lines and set merge.sldb.driver in .git/config (idempotent)")
    d.add_argument("--store", help="Store path (for --install)")
