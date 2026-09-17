from typing import Any

from .sldb_error import SLDBError

class SLDBValidationError(SLDBError):
    """Raised when document validation or idempotency checks fail."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.details = details or {}
