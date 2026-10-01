"""Domain error raised when a graph analysis call is given options it does not accept.

Subclasses `TypeError` as well as `SLDBError`, matching how Python reports an unexpected
keyword argument, so existing callers keep working.
"""

from __future__ import annotations

from .sldb_error import SLDBError


class SLDBGraphArgumentError(SLDBError, TypeError):
    """Raised when graph analysis receives unknown keyword arguments."""
