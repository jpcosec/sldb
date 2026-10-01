"""Domain error raised when a document reference names no document, or more than one.

Subclasses `ValueError` as well as `SLDBError` so the `serve` routes that already map a
`ValueError` to 404 keep their behaviour while library consumers can catch the domain error.
"""

from __future__ import annotations

from .sldb_error import SLDBError


class SLDBDocumentTargetError(SLDBError, ValueError):
    """Raised when a doc ref resolves to zero documents or is ambiguous between several."""
