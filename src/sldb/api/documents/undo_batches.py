"""Undo the last applied batches of a store, from the write journal (`sldb.store.write_journal`):
works from any process, not only the one that applied them."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.documents.apply_batch import _run
from sldb.api.documents.transaction import transaction
from sldb.api.stores.open_store import open_store
from sldb.api.documents.nothing_to_undo import NothingToUndo
from sldb.api.documents.undo_report import UndoReport
from sldb.store import write_journal
from sldb.store.io import store_lock


def undo_batches(store: str | Path | None, steps: int = 1, batch_id: str | None = None, pythonpath: str | None = None) -> UndoReport:
    """Revert the last `steps` not-yet-reverted batches, newest first, in one transaction under one
    lock: whole or nothing. `batch_id` names the batch expected to be the last not reverted; if it
    is not, `NothingToUndo`. A document changed after its batch (its hash differs from the one the
    batch left) raises `ConflictError` and nothing is written. Undoing is a new write (provenance
    is re-stamped) and is not itself a journal batch: the entry is marked reverted."""
    location = open_store(store)
    with store_lock(location.store_path, wait=True):
        chosen, left = _chosen(location.store_path, steps, batch_id)
        with transaction(location.store_path, pythonpath) as tx:
            reports = [_run(location, tx, entry["inverse"], pythonpath, _pins(entry)) for entry in chosen]
        write_journal.mark_reverted(location.store_path, [e["batch_id"] for e in chosen])
        return UndoReport(undone=[e["batch_id"] for e in chosen], saved=[list(r.saved) for r in reports], changes=[e["inverse"] for e in chosen], remaining=left - len(chosen))


def _chosen(store_path: Path, steps: int, batch_id: str | None) -> tuple[list[dict[str, Any]], int]:
    """The entries to revert, newest first, and how many were not reverted; `NothingToUndo` when there are not that many or `batch_id` is not the newest."""
    pending = write_journal.unreverted(store_path)
    if steps < 1 or steps > len(pending):
        raise NothingToUndo(f"asked to undo {steps} batch(es); the store's write journal has {len(pending)} applied batch(es) not yet reverted", len(pending))
    chosen = list(reversed(pending[-steps:]))
    if batch_id is not None and batch_id != chosen[0]["batch_id"]:
        known = any(e["batch_id"] == batch_id for e in write_journal.entries(store_path))
        raise NothingToUndo(f"batch {batch_id} cannot be undone: {'already reverted or not the last not-reverted batch' if known else 'not in the write journal'}; the last not-reverted batch is {chosen[0]['batch_id']}", len(pending))
    return chosen, len(pending)


def _pins(entry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """The provenance each document had before the batch: the undo puts it back, so the store hash returns too."""
    return {d["id"]: d["before"]["provenance"] for d in entry["documents"] if d["before"] and d["before"].get("provenance")}
