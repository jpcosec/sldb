"""Domain error raised when a document payload cannot be written back to its store."""

from __future__ import annotations

from .sldb_error import SLDBError


class SLDBPayloadSaveError(SLDBError):
    """Raised when a payload save names an unregistered model or document, or breaks idempotency."""
