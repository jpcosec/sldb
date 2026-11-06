"""`UnknownKindError`."""

from __future__ import annotations

from sldb.notations.errors.validation_error import ValidationError


class UnknownKindError(ValidationError):
    """Una notación o spec style nombra un kind no declarado por la paleta."""
