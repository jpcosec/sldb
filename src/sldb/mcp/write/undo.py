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
        """Undo the last `steps` proposals apply_changes applied in this session, newest first. The
        contract is 'same content, provenance aside': undoing is a new write, so it re-stamps
        `sldb.at`, `sldb.via` and what derives from them. Each inverse is guarded by the content the
        batch left (the document without its provenance block), so a document someone changed and
        put back to that content is not stale. The `steps` inverses are applied as one chain, under
        one lock and in one transaction, each checked against the state the previous one leaves:
        whole or nothing. If any is refused (`stale`), nothing is written (`written: False`) and the
        stack stays as it was."""
        require(self.level, CONTENT, "undo_changes")
        if steps < 1 or steps > len(self.batches):
            return rejected("nothing_to_undo", f"asked to undo {steps} batch(es); this session has {len(self.batches)} applied batch(es) left to undo (the stack is per session and in memory)", undone=0, remaining=len(self.batches))
        chain = list(reversed(self.batches[-steps:]))
        try:
            reports = api.apply_batches(self.store_path, chain)
        except api.ConflictError as error:
            return rejected("stale", f"the store changed after that batch was applied: {error} Nothing was written; the stack is untouched.", document=error.ref, undone=0, remaining=len(self.batches))
        except Exception as error:
            return {**refusal(error), "undone": 0, "remaining": len(self.batches)}
        del self.batches[-steps:]
        undone = [{"applied": True, "saved": list(report.saved), "changes": changes} for report, changes in zip(reports, chain)]
        return {"applied": True, "undone": len(undone), "batches": undone, "remaining": len(self.batches), "pending": [PENDING["guards_in_transaction"]]}
