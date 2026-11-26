"""The refusal of an undo with no such batch to undo."""

from __future__ import annotations

from sldb.core.exceptions import SLDBError


class NothingToUndo(SLDBError):
    """There is no (such) batch to undo; nothing was written."""

    def __init__(self, message: str, remaining: int) -> None:
        super().__init__(message)
        self.remaining = remaining
