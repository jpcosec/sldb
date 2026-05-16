class SLDBError(Exception):
    """Base exception for all SLDB errors."""

    pass


class SLDBModelError(SLDBError):
    """Raised when there is an issue with a StructuredNLDoc model definition."""

    pass


class SLDBValidationError(SLDBError):
    """Raised when document validation or idempotency checks fail."""

    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details or {}


class SLDBStoreError(SLDBError):
    """Raised when there is an issue with the SLDB store or indexes."""

    pass


class SLDBASTError(SLDBError):
    """Raised when there is an issue parsing or processing the AST."""

    pass


class SLDBLinkError(SLDBError):
    """Raised when links cannot be recovered or composed."""

    pass
