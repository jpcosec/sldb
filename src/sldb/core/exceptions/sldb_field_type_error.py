"""Domain error raised when a field path addresses a value of the wrong shape.

Subclasses `TypeError` as well as `SLDBError` so existing `except TypeError` callers
(the sldb CLI, `serve`'s field routes) keep working while library consumers can catch
the domain error.
"""

from __future__ import annotations

from .sldb_error import SLDBError


class SLDBFieldTypeError(SLDBError, TypeError):
    """Raised when a path's value is not the kind of value the operation needs."""
