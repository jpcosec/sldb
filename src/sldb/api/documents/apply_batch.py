"""Several document changes applied as one: prevalidated together, then written in one
transaction, so a batch applies whole or not at all."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from sldb.api.documents.batch_inverse import before, inverse
from sldb.api.documents.batch_prevalidate import prevalidate_changes
from sldb.api.documents.batch_report import BatchReport
from sldb.api.documents.transaction import Transaction, transaction
from sldb.api.stores.open_store import open_store
from sldb.store.io import store_lock

_ORDER = {"create": 0, "track": 0, "update": 1, "move": 2, "untrack": 3, "delete": 3}
_APPLY: dict[str, Callable[[Transaction, dict[str, Any]], Any]] = {
    "create": lambda tx, c: tx.create(c["model"], c["id"], c["payload"], c.get("path")),
    "track": lambda tx, c: tx.track(c["path"], c["model"], c["id"]),
    "update": lambda tx, c: tx.update(c["id"], c["payload"], c.get("expected_source_hash"), c.get("expected")),
    "move": lambda tx, c: tx.move(c["id"], c["path"]),
    "untrack": lambda tx, c: tx.untrack(c["id"]),
    "delete": lambda tx, c: tx.delete(c["id"]),
}


def apply_batch(store: str | Path | None, changes: list[dict[str, Any]], pythonpath: str | None = None, dry_run: bool = False) -> BatchReport:
    """Prevalidate `changes` and apply them in one transaction, creates and tracks first, then
    updates, moves, and last untracks and deletes (request order within each group).

    Args:
        store: The store (path, alias, or None to discover it).
        changes: One dict per change: `id` (the document name, unique in the batch), `action`
            (`create`, `update`, `move`, `delete`, `track`, `untrack`), and by action `model`
            (create, track), `payload` (create, update), `path` (move, track; optional for
            create, else the model's default directory), and the guards `expected_source_hash`
            `expected_content_hash` (the text without its provenance block) and `expected` (the full current payload) on any action over a tracked document.
        pythonpath: Directory to import the store's model modules from.
        dry_run: Only prevalidate (shape, model, payload round-trip, guards, targets) under the
            lock and return before opening the transaction: nothing is written, the `on_write`
            rules are not evaluated, and the errors are the ones a real apply raises.

    Returns:
        With `dry_run`: a report with `applied=False`, `saved` and `inverse` empty and `planned`
        the ids in the order a real apply would write them.
        Otherwise the ids applied, in order, and `inverse`: the batch that undoes this one, guarded by
        the content hashes this one left (`apply_batch(store, report.inverse)` puts it back).

    Raises:
        SLDBValidationError: A malformed change, or a payload the model rejects (G4).
        ConflictError: A guard that does not match the document's current state.
        SLDBStoreError: A document or file that exists where it must not, or is missing.
        RollbackError: A failure while applying whose rollback could not restore every file.
        The store lock is held (waiting for it) from prevalidation to the last write, so a
        concurrent process cannot change a guarded document in between.
        Nothing is written when prevalidation raises; a failure while applying rolls the
        whole batch back and re-raises.
    """
    location = open_store(store)
    with store_lock(location.store_path, wait=True):  # guards are checked and writes made under one lock
        if dry_run:
            return BatchReport(saved=[], applied=False, planned=[c["id"] for c in _plan(location, changes, pythonpath)])
        with transaction(location.store_path, pythonpath) as tx:
            return _run(location, tx, changes, pythonpath)


def apply_batches(store: str | Path | None, batches: list[list[dict[str, Any]]], pythonpath: str | None = None) -> list[BatchReport]:
    """Apply `batches` one after the other in one transaction under one lock: each batch is
    prevalidated against the state the previous one left, and if any raises, nothing of any
    of them stays written (the exception is `apply_batch`'s). One report per batch, in order.
    This is what lets a chain of inverses touching the same document be checked step by step."""
    location = open_store(store)
    with store_lock(location.store_path, wait=True):
        with transaction(location.store_path, pythonpath) as tx:
            return [_run(location, tx, changes, pythonpath) for changes in batches]


def _run(location: Any, tx: Transaction, changes: list[dict[str, Any]], pythonpath: str | None) -> BatchReport:
    plan = _plan(location, changes, pythonpath)
    prior = before(location, plan, pythonpath)  # what each change replaces, read under the lock
    saved = [_applied(tx, change) for change in plan]
    return BatchReport(saved=saved, inverse=inverse(location, prior))


def _plan(location: Any, changes: list[dict[str, Any]], pythonpath: str | None) -> list[dict[str, Any]]:
    return sorted(prevalidate_changes(location, changes, pythonpath), key=lambda change: _ORDER[change["action"]])


def _applied(tx: Transaction, change: dict[str, Any]) -> str:
    _APPLY[change["action"]](tx, change)
    return change["id"]
