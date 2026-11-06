"""`NotationMismatchError`."""

from __future__ import annotations

from sldb.notations.errors.validation_error import ValidationError


class NotationMismatchError(ValidationError, ValueError):
    """La notación existe pero dibuja un tipo de diagrama distinto al spec."""
