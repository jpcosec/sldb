"""`undo_changes`: the session's stack of inverse batches, applied back with `sldb.api.apply_batch`."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import sldb.api as api
from sldb.mcp.mutability import CONTENT, require
from sldb.mcp.write.apply import refusal, rejected
from sldb.mcp.write.pending import PENDING


class UndoStack:
    """The inverse batch (`BatchReport.inverse`) of every proposal `apply_changes` applied in this
    session, newest last. One per server session, in memory: it is not persisted and there is no redo."""

    def __init__(self, store_path: Path, level: int) -> None:
        self.store_path, self.level = store_path, level
        self.batches: list[list[dict[str, Any]]] = []

    def push(self, inverse: list[dict[str, Any]]) -> None:
        """Keep the inverse of a batch just applied."""
        self.batches.append(list(inverse))

    def undo_changes(self, steps: int = 1) -> dict[str, Any]:
        """Undo the last `steps` proposals apply_changes applied in this session, newest first: each
        one's inverse batch goes through apply_batch with the guards it left, whole or nothing. A
        batch someone else wrote over since is refused (`stale`) with nothing of it written; the
        undo stops there, what was undone stays undone and that batch and the older ones stay."""
        require(self.level, CONTENT, "undo_changes")
        if steps < 1 or steps > len(self.batches):
            return rejected("nothing_to_undo", f"asked to undo {steps} batch(es); this session has {len(self.batches)} applied batch(es) left to undo (the stack is per session and in memory)", undone=0, remaining=len(self.batches))
        undone: list[dict[str, Any]] = []
        for _ in range(steps):
            step = self._undo_last()
            if not step["applied"]:
                return {**step, "written": bool(undone), "undone": len(undone), "batches": undone, "remaining": len(self.batches)}
            undone.append(step)
        return {"applied": True, "undone": len(undone), "batches": undone, "remaining": len(self.batches), "pending": [PENDING["guards_in_transaction"]]}

    def _undo_last(self) -> dict[str, Any]:
        """Apply the newest inverse batch; it leaves the stack only once it was written."""
        inverse = self.batches[-1]
        try:
            report = api.apply_batch(self.store_path, inverse)
        except api.ConflictError as error:
            return rejected("stale", f"the store changed after that batch was applied: {error} It stays in the stack.", document=error.ref)
        except Exception as error:
            return refusal(error)
        self.batches.pop()
        return {"applied": True, "saved": list(report.saved), "changes": inverse}
