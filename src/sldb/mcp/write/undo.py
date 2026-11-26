"""`undo_changes`: the last batches of the store's write journal, reverted with `sldb.api.undo_batches`.
The journal is in the store (docs/architecture/journal-authority.md), so any server process on the
same store can undo what another applied; there is no redo."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import sldb.api as api
from sldb.mcp.mutability import CONTENT, require
from sldb.mcp.write.apply import refusal, rejected
from sldb.mcp.write.pending import PENDING


class UndoStack:
    """The undo of one server over the store's write journal (nothing is kept in memory)."""

    def __init__(self, store_path: Path, level: int) -> None:
        self.store_path, self.level = store_path, level

    def undo_changes(self, steps: int = 1, batch_id: str | None = None) -> dict[str, Any]:
        """Undo the last `steps` not-yet-reverted batches of the store, newest first (by default the
        last one), whoever applied them and in whatever session. With `batch_id`, only if it is the
        last not-reverted batch; otherwise it is refused with the reason. The contract is 'same
        content, provenance aside': undoing is a new write, so it re-stamps `sldb.at`, `sldb.via`.
        A document that changed after its batch (its content hash differs from the one the batch
        left) refuses the undo as `stale`. The `steps` inverses are applied as one chain, in one
        transaction: whole or nothing (`written: False` when refused)."""
        require(self.level, CONTENT, "undo_changes")
        try:
            report = api.undo_batches(self.store_path, steps=steps, batch_id=batch_id)
        except api.NothingToUndo as error:
            return rejected("nothing_to_undo", f"{error} (the write journal is the store's, not the session's)", undone=0, remaining=error.remaining)
        except api.ConflictError as error:
            return rejected("stale", f"the store changed after that batch was applied: {error} Nothing was written.", document=error.ref, undone=0, remaining=self._remaining())
        except Exception as error:
            return {**refusal(error), "undone": 0, "remaining": self._remaining()}
        return self._answer(report)

    @staticmethod
    def _answer(report: api.UndoReport) -> dict[str, Any]:
        undone = [{"batch_id": b, "applied": True, "saved": saved, "changes": changes} for b, saved, changes in zip(report.undone, report.saved, report.changes)]
        return {"applied": True, "undone": len(undone), "batches": undone, "remaining": report.remaining, "pending": [PENDING["guards_in_transaction"]]}

    def _remaining(self) -> int:
        from sldb.store import write_journal

        return len(write_journal.unreverted(self.store_path))
