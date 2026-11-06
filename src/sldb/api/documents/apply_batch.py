"""Several document changes applied as one: prevalidated together, then written in one
transaction, so a batch applies whole or not at all."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from sldb.api.documents.batch_prevalidate import prevalidate_changes
from sldb.api.documents.batch_report import BatchReport
from sldb.api.documents.transaction import Transaction, transaction
from sldb.api.stores.open_store import open_store

_ORDER = {"create": 0, "track": 0, "update": 1, "move": 2, "untrack": 3, "delete": 3}
_APPLY: dict[str, Callable[[Transaction, dict[str, Any]], Any]] = {
    "create": lambda tx, c: tx.create(c["model"], c["id"], c["payload"], c.get("path")),
    "track": lambda tx, c: tx.track(c["path"], c["model"], c["id"]),
    "update": lambda tx, c: tx.update(c["id"], c["payload"]),
    "move": lambda tx, c: tx.move(c["id"], c["path"]),
    "untrack": lambda tx, c: tx.untrack(c["id"]),
    "delete": lambda tx, c: tx.delete(c["id"]),
}


def apply_batch(store: str | Path | None, changes: list[dict[str, Any]], pythonpath: str | None = None) -> BatchReport:
    """Prevalidate `changes` and apply them in one transaction, creates and tracks first, then
    updates, moves, and last untracks and deletes (request order within each group).

    Args:
        store: The store (path, alias, or None to discover it).
        changes: One dict per change: `id` (the document name, unique in the batch), `action`
            (`create`, `update`, `move`, `delete`, `track`, `untrack`), and by action `model`
            (create, track), `payload` (create, update), `path` (move, track; optional for
            create, else the model's default directory), and the guards `expected_source_hash`
            and `expected` (the full current payload) on any action over a tracked document.
        pythonpath: Directory to import the store's model modules from.

    Returns:
        The ids applied, in order.

    Raises:
        SLDBValidationError: A malformed change, or a payload the model rejects (G4).
        ConflictError: A guard that does not match the document's current state.
        SLDBStoreError: A document or file that exists where it must not, or is missing.
        RollbackError: A failure while applying whose rollback could not restore every file.
        Nothing is written when prevalidation raises; a failure while applying rolls the
        whole batch back and re-raises.
    """
    location = open_store(store)
    plan = sorted(prevalidate_changes(location, changes, pythonpath), key=lambda change: _ORDER[change["action"]])
    with transaction(location.store_path, pythonpath) as tx:
        saved = [_applied(tx, change) for change in plan]
    return BatchReport(saved=saved)


def _applied(tx: Transaction, change: dict[str, Any]) -> str:
    _APPLY[change["action"]](tx, change)
    return change["id"]
