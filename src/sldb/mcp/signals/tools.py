"""`list_signals`: the log of requests for what does not exist, paged like every set."""

from __future__ import annotations

from typing import Any

from sldb.mcp.paging import DEFAULT_LIMIT, page
from sldb.mcp.signals.catalog import CLASSES
from sldb.mcp.signals.log import SignalLog


class SignalTools:
    """The one tool over the signal log; served at every level (the log is not store state)."""

    def __init__(self, log: SignalLog) -> None:
        self.log = log

    def list_signals(self, signal_class: str | None = None, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """List the signals registered so far (requests for what does not exist or is called differently), oldest first; optionally of one `signal_class`."""
        if signal_class is not None and signal_class not in CLASSES:
            raise ValueError(f"signal_class must be one of {CLASSES}, not {signal_class!r}")
        entries = [e for e in self.log.entries() if signal_class in (None, e.get("signal_class"))]
        return page(entries, offset, limit, None if entries else "no signal registered")
