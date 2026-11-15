"""Requests for what does not exist, or is called differently, are signals: logged, answered
with near names from `sldb.api.matching`, and readable through `list_signals`. They are not errors."""

from sldb.mcp.signals.catalog import CLASSES, PENDING_TOOLS
from sldb.mcp.signals.log import SignalLog
from sldb.mcp.signals.settle import settle, signalled
from sldb.mcp.signals.tools import SignalTools

__all__ = ["CLASSES", "PENDING_TOOLS", "SignalLog", "SignalTools", "settle", "signalled"]
