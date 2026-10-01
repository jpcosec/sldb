"""Domain error raised when a dotted field path does not address a value in a payload.

Subclasses `KeyError` as well as `SLDBError` so library consumers can catch the domain
error while callers that already handle `KeyError` (the sldb CLI, `serve`'s field routes)
keep working unchanged.
"""

from __future__ import annotations

from .sldb_error import SLDBError


class SLDBFieldPathError(SLDBError, KeyError):
    """Raised when a field path is empty, names a missing key, or steps into a scalar."""

    def __str__(self) -> str:
        return SLDBError.__str__(self)
