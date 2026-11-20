"""Move a file or directory and keep the store and the repo's references to it true."""

from __future__ import annotations

from pathlib import Path

from sldb.api.documents.move_path_apply import apply_plan
from sldb.api.documents.move_path_plan import build_plan
from sldb.api.documents.move_path_report import MovePathReport
from sldb.api.documents.transaction import transaction
from sldb.api.stores.open_store import open_store


def move_path(store: str | Path | None, source: str | Path, destination: str | Path, *, dry_run: bool = False, pythonpath: str | None = None) -> MovePathReport:
    """Move `source` to `destination` (a file or a directory) inside the project, in one transaction.

    The file moves with `git mv` when git versions it, else on disk. Tracked documents under it
    stay tracked under their names (`move_document`). Every field of a tracked document whose value
    is the old path, or starts with it plus `/` for a directory, takes the new path, written through
    `Transaction.update`. Inline Markdown links in the repo's `.md` files that point at the old path
    point at the new one. If anything fails the tree and the store are as they were.

    Args:
        store: The store (path, alias, or None to discover it).
        source: What to move; relative to the project root, or absolute inside it.
        destination: Where it goes; must not exist and must stay inside the project root.
        dry_run: Only report what would move and be rewritten; nothing is touched.
        pythonpath: Directory to import the store's model modules from.

    Returns:
        A `MovePathReport`: each file moved, each field rewritten (`document`, `field`, `old`,
        `new`) and each link rewritten (`file`, `line`, `old`, `new`).

    Raises:
        SLDBStoreError: `source` is missing, `destination` exists or leaves the project root, or
            `source` holds the project root or the store; nothing is touched.
        SLDBValidationError: A rewritten document no longer validates; everything is restored.
    """
    location = open_store(store, mode="readonly" if dry_run else "default")
    plan = build_plan(location, source, destination, pythonpath)
    if not dry_run:
        with transaction(location.store_path, pythonpath) as tx:
            apply_plan(tx, plan)
    return plan.report(dry_run)
